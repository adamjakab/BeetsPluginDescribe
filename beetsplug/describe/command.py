#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 3/21/20, 11:28 AM
#  License: See LICENSE.txt

from optparse import OptionParser
import numpy as np
import pandas as pd
import termplotlib as tpl
import termtables as tt
from beets import library

from beets.dbcore import types
from beets.library import Library, Item, parse_query_parts
from beets.ui import Subcommand, decargs
from beets.util.confit import Subview

from beetsplug.describe import common

# The plugin
__PLUGIN_NAME__ = u'describe'
__PLUGIN_SHORT_DESCRIPTION__ = u'describe a library item field'


class DescribeCommand(Subcommand):
    config: Subview = None
    lib: Library = None
    query = None
    parser: OptionParser = None

    def __init__(self, cfg):
        self.config = cfg

        self.parser = OptionParser(usage='beet describe field [options] [QUERY...]')

        self.parser.add_option(
            '-v', '--version',
            action='store_true', dest='version', default=False,
            help=u'show plugin version'
        )

        # Keep this at the end
        super(DescribeCommand, self).__init__(
            parser=self.parser,
            name=__PLUGIN_NAME__,
            help=__PLUGIN_SHORT_DESCRIPTION__
        )

    def func(self, lib: Library, options, arguments):
        self.lib = lib
        self.query = decargs(arguments)

        # You must either pass a training name or request listing
        if len(self.query) < 1:
            self.parser.print_help()
            return

        if options.version:
            self.show_version_information()
            return

        self.handle_display()

    def handle_display(self):
        field_to_examine = self.query.pop(0)
        fields = [field_to_examine]

        # field_to_examine = "genre"
        # fields = ["id", "bpm", "year", "country", "acoustid_id", "mood_aggressive", field_to_examine]

        lib_items = self._retrieve_library_items()
        data = self._extract_data_from_items(lib_items, fields)
        data_desc = self._describe(data, field_to_examine)

        self.print_describe_table(data_desc)
        self.plot_field_data(data_desc)

    def print_describe_table(self, desc):
        table_data = []
        for key in desc:
            data = desc[key]
            if "label" in data and "value" in data:
                table_data.append([data["label"], data["value"]])

        tt.print(
            table_data,
            header=["Name", "Value"],
            padding=(0, 1),
            alignment="lr"
        )

    def plot_field_data(self, desc):
        field_name = desc["field_name"]["value"]
        field_type = desc["field_type"]["value"]
        field_type_auto = desc["field_type_auto"]["value"]
        df = desc["df"]
        vec = df[field_name]

        if common.is_numeric(field_type, field_type_auto):
            vec = pd.to_numeric(vec, errors='coerce').fillna(0)

            # todo: put option/config for bins
            num_bins = 10

            self._say("Distribution(bins={bins}) histogram".format(bins=num_bins),
                      log_only=False)

            bins = np.linspace(vec.min(), vec.max(), (num_bins + 1))
            closed_bins = list(bins[:-1])
            groups = df.groupby(np.digitize(vec, closed_bins))

            values = list(groups[field_name].count())

            bin_values = list(bins)
            keys = []
            for i in range(0, len(closed_bins)):
                low = str(round(float(bin_values[i]), 1))
                high = str(round(float(bin_values[i + 1]), 1))
                key = "{} - {}".format(low, high)
                keys.append(key)
        else:
            self._say("Unique element histogram", log_only=False)
            vc: pd.Series = vec.value_counts(sort=True, dropna=False)
            keys = list(vc.keys())
            values = vc.values

        fig = tpl.figure()
        fig.barh(values, keys, force_ascii=False)
        fig.show()

    def _describe(self, data, field):
        desc = {}

        df = pd.DataFrame(data)
        vec = df[field]

        # Field name
        desc["field_name"] = {'label': 'Field name', 'value': field}

        # Store the DataFrame
        desc["df"] = df

        # Field type
        field_type = common.get_field_type(field)
        desc["field_type"] = {'label': 'Field type', 'value': field_type}

        # Field type Auto
        field_type_auto = None
        if not field_type:
            field_type_auto = common.get_automatic_type_for_field(field)
        desc["field_type_auto"] = {'label': 'Auto type', 'value': field_type_auto}

        # Total count
        total_count = vec.count()
        desc["total_count"] = {'label': 'Count', 'value': total_count}

        if common.is_numeric(field_type, field_type_auto):
            vec = pd.to_numeric(vec, errors='coerce').dropna()

            # Min
            min = vec.min()
            desc["min"] = {'label': 'Min', 'value': min}

            # Max
            max = vec.max()
            desc["max"] = {'label': 'Max', 'value': max}

            # Mean
            mean = vec.mean()
            desc["mean"] = {'label': 'Mean', 'value': mean}

            # Median
            median = vec.median()
            desc["median"] = {'label': 'Median', 'value': median}

            # Null Count (na is dropped on vec)
            null_count = total_count - vec.count()
            desc["null_count"] = {'label': 'Empty', 'value': null_count}
        else:
            vc: pd.Series = vec.value_counts(sort=True, dropna=False)

            # Unique count
            unique_count = vc.count()
            desc["unique_count"] = {'label': 'Unique', 'value': unique_count}

            # Unique First
            unique_keys = list(vc.keys())
            unique_first_key = unique_keys[0]
            unique_first_val = vc.max()
            unique_first_str = "{}({})".format(unique_first_key, unique_first_val)
            desc["unique_first"] = {'label': 'Most frequent', 'value': unique_first_str}

            # Unique First
            unique_last_key = unique_keys[-1]
            unique_last_val = vc.min()
            unique_last_str = "{}({})".format(unique_last_key, unique_last_val)
            desc["unique_last"] = {'label': 'Least frequent', 'value': unique_last_str}

            null_count = (df[field] == '').sum()
            desc["null_count"] = {'label': 'Empty', 'value': null_count}

        return desc

    def _extract_data_from_items(self, items, fields):
        data = []

        for item in items:
            item: Item
            item_data = {}

            for field in fields:
                item_data[field] = item.get(field, default="")

            data.append(item_data)

        return data

    def _retrieve_library_items(self):
        full_query = self.query

        # parsed_query = parse_query_string(" ".join(full_query), Item)[0]
        parsed_query = parse_query_parts(full_query, Item)[0]

        self._say("Selection query: {}".format(parsed_query), log_only=True)

        return self.lib.items(parsed_query)

    def show_version_information(self):
        from beetsplug.describe.version import __version__
        self._say("Plot(beets-{}) plugin for Beets: v{}".format(__PLUGIN_NAME__, __version__))

    def _say(self, msg, log_only=False):
        common.say(msg, log_only)
