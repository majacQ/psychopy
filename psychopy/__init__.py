#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2021 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

# --------------------------------------------------------------------------
# This file is automatically generated during build (do not edit directly).
# --------------------------------------------------------------------------

import os
import sys

__version__ = '2021.1.4'
__license__ = 'GNU GPLv3 (or more recent equivalent)'
__author__ = 'Jonathan Peirce'
__author_email__ = 'jon.peirce@gmail.com'
__maintainer_email__ = 'jon.peirce@gmail.com'
__url__ = 'https://www.psychopy.org/'
__download_url__ = 'https://github.com/psychopy/psychopy/releases/'
__git_sha__ = 'n/a'
__build_platform__ = 'n/a'

__all__ = ["gui", "misc", "visual", "core",
           "event", "data", "sound", "microphone"]

# for developers the following allows access to the current git sha from
# their repository
if __git_sha__ == 'n/a':
    from subprocess import check_output, PIPE
    # see if we're in a git repo and fetch from there
    try:
        thisFileLoc = os.path.split(__file__)[0]
        output = check_output(['git', 'rev-parse', '--short', 'HEAD'],
                              cwd=thisFileLoc, stderr=PIPE)
    except Exception:
        output = False
    if output:
        __git_sha__ = output.strip()  # remove final linefeed

# update preferences and the user paths
if 'installing' not in locals():
    from psychopy.preferences import prefs
    for pathName in prefs.general['paths']:
        sys.path.append(pathName)

    from psychopy.tools.versionchooser import useVersion, ensureMinimal

# import readline here to get around an issue with sounddevice
# issues GH-2230 GH-2344 GH-2662
try:
    import readline
except ImportError:
    pass  # all that will happen is the stderr/stdout might get redirected

