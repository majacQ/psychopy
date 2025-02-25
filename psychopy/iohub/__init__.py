#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# Part of the psychopy.iohub library.
# Copyright (C) 2012-2016 iSolver Software Solutions
# Distributed under the terms of the GNU General Public License (GPL).
from __future__ import division, absolute_import, print_function

import sys
from .errors import print2err, printExceptionDetailsToStdErr
from .util import module_directory

if sys.platform == 'darwin':
    import objc  # pylint: disable=import-error

EXP_SCRIPT_DIRECTORY = ''


def _localFunc():
    return None


IOHUB_DIRECTORY = module_directory(_localFunc)

_DATA_STORE_AVAILABLE = False
try:
    import tables
    _DATA_STORE_AVAILABLE = True
except ImportError:
    print2err('WARNING: pytables package not found. ',
              'ioHub functionality will be disabled.')
except Exception:
    printExceptionDetailsToStdErr()

from psychopy.iohub.constants import EventConstants, KeyboardConstants, MouseConstants

lazyImports = """
from psychopy.iohub.client.connect import launchHubServer
from psychopy.iohub.devices.computer import Computer
"""

try:
    from psychopy.contrib.lazy_import import lazy_import
    lazy_import(globals(), lazyImports)
except Exception:
    exec(lazyImports)
