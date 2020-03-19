#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 12:29 PM
#  License: See LICENSE.txt
#

import logging
import sys

__logger__ = logging.getLogger('beets.goingrunning')


def say(msg, log_only=False):
    """Log and write to stdout
    """
    __logger__.debug(msg)
    if not log_only:
        sys.stdout.write(msg + "\n")
