# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:20:49 2017

@author: mrbki
"""
from __future__ import absolute_import, print_function

import json
from os import path
from pathlib import Path
from psychopy.experiment.components import (BaseComponent, Param, getInitVals,
                                            _translate)
# overwrite (filemode='w') a detailed log of the last run in this dir
# lastLog = logging.LogFile("lastRun.log", level=logging.DEBUG, filemode='w')
from ..emotiv_record import CORTEX_OBJ
from psychopy.localization import _localized as __localized
_localized = __localized.copy()

_localized.update({'marker_label': _translate('Marker Label'),
                   'marker_value': _translate('Marker Value'),
                   'stop_marker': _translate('Stop Marker')})


class EmotivMarkingComponent(BaseComponent):  # or (VisualComponent)

    categories = ['Custom']
    targets = ['PsychoPy', 'PsychoJS']
    iconFile = Path(__file__).parent / 'emotiv_marking.png'
    tooltip = _translate('Mark a period of EEG')

    def __init__(self, exp, parentName, name='eeg_marker',
                 startType='time (s)', startVal=0.0,
                 stopType='duration (s)', stopVal=1,
                 startEstim='', durationEstim='0.1',
                 label='label', value='1',
                 stop_marker=False):
        super(EmotivMarkingComponent, self).__init__(
            exp, parentName, name=name,
            startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal,
            startEstim=startEstim, durationEstim=0.01)

        # params
        _allow2 = ['constant', 'set every repeat']  # list
        msg = _translate(
            "Label of the marker to be inserted (interpreted as a string)")
        self.params['marker_label'] = Param(
            label, valType='str', inputType="single", categ='Basic',
            updates='constant', allowedUpdates=_allow2[:],
            hint=msg,
            label=_localized['marker_label'])

        msg = _translate(
            "Value of the marker to be inserted (interpreted as a string)")
        self.params['marker_value'] = Param(
            value, valType='str', inputType="single", categ='Basic',
            updates='constant', allowedUpdates=_allow2[:],
            hint=msg,
            label=_localized['marker_value'])

        msg = _translate("Check this box to include a stop marker")
        self.params['stop_marker'] = Param(
            stop_marker, valType='bool', inputType="bool", categ='Basic',
            allowedVals=[True, False],
            updates='constant', allowedUpdates=[],
            hint=msg,
            label=_localized["stop_marker"])

        self.type = 'EmotivMarking'
        self.exp.requireImport(importName='emotiv',
                               importFrom='psychopy.hardware')
        self.order += ['marker_label', 'marker_value', 'stop_marker']

    def writeInitCode(self, buff):
        buff.writeIndented("# This is generated by writeInitCode\n")
        # replace variable params with defaults
        inits = getInitVals(self.params, 'PsychoPy')
        code = ('{} = visual.BaseVisualStim('.format(inits['name']) +
                'win=win, name="{}")\n'.format(inits['name'])
                )
        buff.writeIndentedLines(code)

    def writeInitCodeJS(self, buff):
        inits = getInitVals(self.params, 'PsychoJS')
        obj = {"status": "PsychoJS.Status.NOT_STARTED"}
        code = '{} = {};\n'
        buff.writeIndentedLines(
            code.format(inits['name'], json.dumps(obj)))
        # check for NoneTypes
        for param in inits:
            if inits[param] in [None, 'None', '']:
                inits[param].val = 'undefined'
                if param == 'text':
                    inits[param].val = ""

    def writeStartCode(self, buff):
        buff.writeIndented("# This is generated by the writeStartCode\n")

    def writeRoutineStartCode(self, buff):
        buff.writeIndented("# This is generated by the writeRoutineStartCode\n")

    def writeRoutineEndCode(self, buff):
        buff.writeIndented("# This is generated by the writeRoutineEndCode\n")

    def writeFrameCode(self, buff):
        self.writeStartTestCode(buff)
        code = f"{self.params['name']}.status = STARTED\n"
        buff.writeIndented(code)
        code = ("delta_time = tThisFlip-t  "
                "# Adding the extra time between now and the next screen flip"
                "\n")
        buff.writeIndented(code)
        self.writeParamUpdates(buff, 'set every frame')
        code = ("{}.inject_marker(value=str({}), label={}, "
                "delta_time=delta_time)\n"
                .format(CORTEX_OBJ,
                        self.params['marker_value'],
                        self.params['marker_label']))
        buff.writeIndented(code)
        code = "{}.start_sent = True\n".format(self.params["name"])
        buff.writeIndented(code)
        buff.setIndentLevel(-1, relative=True)

        # test for stop (only if there was some setting for duration or stop)
        if self.params['stopVal'].val not in ('', None, -1, 'None'):
            # writes an if statement to determine whether to draw etc
            self.writeStopTestCode(buff)
            self.writeParamUpdates(buff, 'set every frame')
            code = "{}.status = FINISHED\n".format(self.params['name'])
            buff.writeIndented(code)
            if self.params['stop_marker'].val:
                code = ("delta_time = tThisFlip-t  "
                        "# Adding the extra time between now and the next "
                        "screen flip\n")
                buff.writeIndented(code)
                code = ("{}.update_marker(label={}, delta_time=delta_time)\n"
                        .format(CORTEX_OBJ, self.params['marker_label']))
                buff.writeIndented(code)
            buff.setIndentLevel(-1, relative=True)
        buff.setIndentLevel(-1, relative=True)

    def writeFrameCodeJS(self, buff):
        """Write the code that will be called every frame
        """
        buff.writeIndentedLines(f"\n// {self.params['name']} updates\n")
        # writes an if statement to determine whether to draw etc
        self.writeStartTestCodeJS(buff)
        buff.writeIndented('psychoJS.window.callOnFlip(function() {\n')
        buff.setIndentLevel(1, relative=True)
        buff.writeIndented('if (typeof emotiv != "undefined") {\n')
        buff.setIndentLevel(1, relative=True)
        buff.writeIndented(f'emotiv.sendMarker({self.params["marker_value"]}, {self.params["marker_label"]}, {self.params["stop_marker"]})\n')
        buff.setIndentLevel(-1, relative=True);
        buff.writeIndented("}\n");
        buff.setIndentLevel(-1, relative=True);
        buff.writeIndented('});\n')
        buff.writeIndented('{}.status = PsychoJS.Status.STARTED;\n'
                           .format(self.params['name']))
        # buff.writeIndented("%(name)s.setAutoDraw(true);\n" % self.params)
        # to get out of the if statement
        buff.setIndentLevel(-1, relative=True)
        buff.writeIndented("}\n\n")

        # test for stop (only if there was some setting for duration or stop)
        if self.params['stopVal'].val not in ('', None, -1, 'None'):
            # writes an if statement to determine whether to draw etc
            self.writeStopTestCodeJS(buff)
            buff.writeIndented('psychoJS.window.callOnFlip(function() {\n')
            buff.setIndentLevel(1, relative=True)
            buff.writeIndented('if (typeof emotiv != "undefined") {\n')
            buff.setIndentLevel(1, relative=True)
            buff.writeIndented('emotiv.sendStopMarker()\n')
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('}\n')
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('});\n')
            buff.writeIndented('{}.status = PsychoJS.Status.FINISHED;\n'
                               .format(self.params['name']))

        # buff.writeIndented("%(name)s.setAutoDraw(false);\n" % self.params)
            # to get out of the if statement
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented("}\n")

        # set parameters that need updating every frame
        # do any params need updating? (this method inherited from _base)
        if self.checkNeedToUpdate('set every frame'):
            code = ("\nif (%(name)s.status === PsychoJS.Status.STARTED){ "
                    "// only update if being drawn\n")
            buff.writeIndentedLines(code % self.params)
            buff.setIndentLevel(+1, relative=True)  # to enter the if block
            self.writeParamUpdatesJS(buff, 'set every frame')
            buff.setIndentLevel(-1, relative=True)  # to exit the if block
            buff.writeIndented("}\n")
