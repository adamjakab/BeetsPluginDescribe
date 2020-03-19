#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 11:30 AM
#  License: See LICENSE.txt
#
import os

from beets.plugins import BeetsPlugin
from beets.util.confit import ConfigSource, load_yaml

from beetsplug.plot.command import PlotCommand


class GoingRunningPlugin(BeetsPlugin):
    _default_plugin_config_file_name_ = 'config_default.yml'

    def __init__(self):
        super(GoingRunningPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), self._default_plugin_config_file_name_)
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)

    def commands(self):
        return [PlotCommand(self.config)]
