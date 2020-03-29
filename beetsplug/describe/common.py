#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 3/21/20, 11:28 AM
#  License: See LICENSE.txt

import logging
import os
import sys

from beets import library
from beets.dbcore import types
from beets.library import Item

# Get values as: plg_ns['__PLUGIN_NAME__']
plg_ns = {}
about_path = os.path.join(os.path.dirname(__file__), u'about.py')
with open(about_path) as about_file:
    exec(about_file.read(), plg_ns)

__logger__ = logging.getLogger(
    'beets.{plg}'.format(plg=plg_ns['__PLUGIN_NAME__']))

KNOWN_NUMERIC_FLEX_ATTRIBUTES = [
    "average_loudness",
    "chords_changes_rate",
    "chords_number_rate",
    "danceable",
    "key_strength",
    "mood_acoustic",
    "mood_aggressive",
    "mood_electronic",
    "mood_happy",
    "mood_party",
    "mood_relaxed",
    "mood_sad",
    "rhythm",
    "tonal",
]


def is_numeric(field_type, field_type_auto):
    if field_type:
        f_numeric = field_type in get_dbcore_numeric_types()
    else:
        f_numeric = field_type_auto in get_dbcore_numeric_types()

    return f_numeric


def get_automatic_type_for_field(field):
    field_type = types.String

    if field in KNOWN_NUMERIC_FLEX_ATTRIBUTES:
        field_type = types.Float

    type_name = "{}.{}".format(field_type.__module__, field_type.__name__)

    print("TYPE({}): {}".format(field, field_type))

    return type_name


def get_dbcore_numeric_types():
    type_classes = []

    dbcore_types = [
        types.Integer,
        types.Float,
        types.NullFloat,
        types.PaddedInt,
        types.NullPaddedInt,
        types.ScaledInt,
        library.DurationType
    ]

    for dt in dbcore_types:
        type_classes.append("{}.{}".format(dt.__module__, dt.__name__))

    return type_classes


def get_field_type(field):
    fld_type = None

    # Field types declared by Item
    if field in Item._fields:
        ft = Item._fields[field]
        fld_type = "{}.{}".format(ft.__module__, ft.__class__.__name__)

    # Field types declared/overridden by Plugins
    if not fld_type:
        if field in Item._types:
            ft = Item._types[field]
            fld_type = "{}.{}".format(ft.__module__, ft.__class__.__name__)

    return fld_type


def say(msg, log_only=True, is_error=False):
    _level = logging.DEBUG
    _level = _level if log_only else logging.INFO
    _level = _level if not is_error else logging.ERROR
    __logger__.log(level=_level, msg=msg)
