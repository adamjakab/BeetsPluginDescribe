#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 11:32 AM
#  License: See LICENSE.txt
#


from optparse import OptionParser
import numpy as np
import pandas as pd
import termplotlib as tpl
import termtables as tt

from beets import library
from beets.dbcore import types
from beets.dbcore.db import Results
from beets.dbcore.queryparse import parse_query_part
from beets.library import Library, Item, parse_query_string
from beets.ui import Subcommand, decargs
from beets.util.confit import Subview, NotFoundError

from beetsplug.plot import common

# The plugin
__PLUGIN_NAME__ = u'plot'
__PLUGIN_SHORT_DESCRIPTION__ = u'visualize what you\'ve got in your library'


class PlotCommand(Subcommand):
    config: Subview = None
    lib: Library = None
    query = None
    parser: OptionParser = None

    def __init__(self, cfg):
        self.config = cfg

        self.parser = OptionParser(usage='beet plot [options] [QUERY...]')

        self.parser.add_option(
            '-v', '--version',
            action='store_true', dest='version', default=False,
            help=u'show plugin version'
        )

        # Keep this at the end
        super(PlotCommand, self).__init__(
            parser=self.parser,
            name=__PLUGIN_NAME__,
            help=__PLUGIN_SHORT_DESCRIPTION__
        )

    def func(self, lib: Library, options, arguments):
        self.lib = lib
        self.query = decargs(arguments)

        if options.version:
            self.show_version_information()
            return

        self.handle_display()

    def handle_display(self):
        field_to_examine = "genre"
        # field_to_examine = self.query.pop(0)

        fields = ["id", "bpm", "year", "country", "acoustid_id", "mood_aggressive", field_to_examine]
        lib_items = self._retrieve_library_items()
        data = self._extract_data_from_items(lib_items, fields)

        self.print_describe_table(data, field_to_examine)
        self.plotit(data, field_to_examine)

    def _describe(self, data, field):
        desc = {}

        df = pd.DataFrame(data)
        field_vector = df[field]
        uc: pd.Series = field_vector.value_counts(sort=True, dropna=False)

        # Field name
        desc["field_name"] = {'label': 'Field name', 'value': field}

        # Field type
        field_type = self._get_field_type(field)
        desc["field_type"] = {'label': 'Field type', 'value': field_type}

        # Total count
        total_count = df[field].count()
        desc["total_count"] = {'label': 'Count', 'value': total_count}

        # Min
        if field_type in self._get_dbcore_numeric_types():
            min = field_vector.min()
            desc["min"] = {'label': 'Min', 'value': min}

        # Max
        if field_type in self._get_dbcore_numeric_types():
            max = field_vector.max()
            desc["max"] = {'label': 'Max', 'value': max}

        # Mean
        if field_type in self._get_dbcore_numeric_types():
            mean = field_vector.mean()
            desc["mean"] = {'label': 'Mean', 'value': mean}

        # Median
        if field_type in self._get_dbcore_numeric_types():
            median = field_vector.median()
            desc["median"] = {'label': 'Median', 'value': median}

        if field_type in self._get_dbcore_numeric_types():
            null_count = (df[field].isna()).sum()
        else:
            null_count = (df[field] == '').sum()
        desc["null_count"] = {'label': 'Empty', 'value': null_count}

        # Unique count
        unique_count = uc.count()
        desc["unique_count"] = {'label': 'Unique', 'value': unique_count}

        # Unique First
        unique_keys = list(uc.keys())
        unique_first_key = unique_keys[0]
        unique_first_val = uc.max()
        unique_first_str = "{}({})".format(unique_first_key, unique_first_val)
        desc["unique_first"] = {'label': 'Most frequent', 'value': unique_first_str}

        # Unique First
        unique_last_key = unique_keys[-1]
        unique_last_val = uc.min()
        unique_last_str = "{}({})".format(unique_last_key, unique_last_val)
        desc["unique_last"] = {'label': 'Least frequent', 'value': unique_last_str}

        return desc

    def print_describe_table(self, data, field):
        desc = self._describe(data, field)

        table_data = []
        for key in desc:
            data = desc[key]
            table_data.append([data["label"], data["value"]])

        tt.print(
            table_data,
            header=["Name", "Value"],
            padding=(0, 1),
            alignment="lr"
        )

    def plotit(self, data, field):
        df = pd.DataFrame(data, columns=["id", field])

        uc: pd.Series = df[field].value_counts(sort=True, dropna=False)

        self._say("Plotting attribute: {}".format(field), log_only=False)
        fig = tpl.figure()
        fig.barh(uc.values, list(uc.keys()), force_ascii=False)
        fig.show()

    def _get_dbcore_numeric_types(self):
        type_classes = []

        dbcore_types = [
            types.Integer,
            types.Float,
            types.NullFloat,
            types.PaddedInt,
            types.NullPaddedInt,
            types.ScaledInt
        ]

        for dt in dbcore_types:
            type_classes.append("{}.{}".format(dt.__module__, dt.__name__))

        return type_classes

    def _get_field_type(self, field):
        fld_type = None

        if field in Item._fields:
            ft = Item._fields[field]
            fld_type = "{}.{}".format(ft.__module__, ft.__class__.__name__)

        return fld_type

    def _extract_data_from_items(self, items, fields):
        data = []

        for item in items:
            item_data = {}

            for field in fields:
                item_data[field] = item.get(field, default="")

            data.append(item_data)

        return data

    def _retrieve_library_items(self):
        full_query = self.query
        parsed_query = parse_query_string(" ".join(full_query), Item)[0]
        self._say("Song selection query: {}".format(parsed_query), log_only=False)

        return self.lib.items(parsed_query)

    def show_version_information(self):
        from beetsplug.plot.version import __version__
        self._say("Plot(beets-{}) plugin for Beets: v{}".format(__PLUGIN_NAME__, __version__))

    def _say(self, msg, log_only=False):
        common.say(msg, log_only)
