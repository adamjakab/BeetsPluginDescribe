#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 11:32 AM
#  License: See LICENSE.txt
#


from optparse import OptionParser
import numpy as np
import termplotlib as tpl

from beets import library
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
        field_to_examine = self.query.pop(0)
        items = self._retrieve_library_items()
        self.plotit(items, field_to_examine)

    def plotit(self, items, field):
        sample = []
        for item in items:
            if item.get(field):
                sample.append(float(item.get(field)))

        sample = np.array(sample)

        counts, bin_edges = np.histogram(sample, bins=10)

        self._say("Displaying: {}".format(field), log_only=False)
        fig = tpl.figure()
        fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False, strip=True)
        fig.show()

    def _retrieve_library_items(self):
        full_query = self.query
        parsed_query = parse_query_string(" ".join(full_query), Item)[0]
        self._say("Song selection query: {}".format(parsed_query), log_only=True)

        return self.lib.items(parsed_query)

    def show_version_information(self):
        from beetsplug.plot.version import __version__
        self._say("Plot(beets-{}) plugin for Beets: v{}".format(__PLUGIN_NAME__, __version__))

    def _say(self, msg, log_only=False):
        common.say(msg, log_only)
