#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gc_cursor_demo/run.py

Demonstrates the ioHub Common EyeTracking Interface by displaying a gaze cursor
at the currently reported gaze position on an image background.

Update the iohub_config.yaml in this directory and uncomment the config settings
for the eye tracker to be used.
"""

from __future__ import absolute_import, division, print_function

from psychopy import core, visual
from psychopy.data import TrialHandler, importConditions
from psychopy.iohub import launchHubServer
from psychopy.iohub.util import getCurrentDateTimeString
import os

if __name__ == "__main__":
    """
    The run method contains your experiment logic. In this example we:

    1) Load an xlsx file containing the trial conditions for use
       during the experiment. All DV's and IV's to be used or updated
       for each trial must be specified as columns in the xlsx file.
    2) Inform the ioDataStore of the trial conditions to be used, resulting in the
       creation of an experiment specific results table, with a field for each
       DV and IV defined in the xls file.
    3) Run the eye tracking device's runSetupProcedure(), which allows
       the calibration, validation, etc. of the eye tracking system being used.
    4) Create the experiment runtime graphics, including creating a cache of
       images to be displayed for each trial of the experiment.
    5) Run the experimental block of trials of the demo. Each trial sequence
       consists of:
           a) The participant pressing the SPACE key to start the trial.
           b) Randomly displaying one of the background images for a trial.
           c) Starting recording of data from the eye tracker.
           d) Displaying a gaze contingent dot located at the gaze position reported by the eye tracker.
           e) Ending each trial by pressing the SPACE key.
           f) Sending any condition variable value changes for that trial
              to the ioDataStore for easy future selection of device events
              recorded during the trial or for specific condition variable values.
           g) Stopping of event recording on the eye tracker device.
    """

    exp_conditions = importConditions('trial_conditions.xlsx')
    trials = TrialHandler(exp_conditions, 1)

    io_hub = launchHubServer(experiment_code='gc_cursor', iohub_config_name="iohub_config.yaml")

    # Inform the ioDataStore that the experiment is using a
    # TrialHandler. The ioDataStore will create a table
    # which can be used to record the actual trial variable values (DV or IV)
    # in the order run / collected.
    #
    io_hub.createTrialHandlerRecordTable(trials)

    # Let's make some short-cuts to the devices we will be using
    # in this demo.
    tracker = None
    try:
        tracker = io_hub.devices.tracker
    except Exception:
        print(" No eye tracker config found in iohub_config.yaml")
        io_hub.quit()
        core.quit()

    display = io_hub.devices.display
    kb = io_hub.devices.keyboard

    # Start by running the eye tracker default setup / calibration.
    #
    tracker.runSetupProcedure()

    # Create a psychopy window for the experiment graphics,
    # ioHub supports the use of one full screen window during
    # the experiment runtime. (If you are using a window at all).
    #
    res = display.getPixelResolution()  # Current pixel resolution of the Display to be used
    coord_type = display.getCoordinateType()
    window = visual.Window(res, monitor=display.getPsychopyMonitorName(),  # name of the PsychoPy Monitor Config file.
                           units=coord_type,  # coordinate space to use.
                           fullscr=True,  # We need full screen mode.
                           allowGUI=False,  # We want it to be borderless
                           screen=display.getIndex())  # The display index to use, assuming a multi display setup.
    window.setMouseVisible(False)

    # Create a dict of image stim for trials and a gaze blob to show the
    # reported gaze position with.
    #
    image_cache = dict()
    image_names = ['canal.jpg', 'fall.jpg', 'party.jpg', 'swimming.jpg', 'lake.jpg']
    for iname in image_names:
        image_cache[iname] = visual.ImageStim(window, image=os.path.join('./images/', iname), name=iname,
                                              units=coord_type)

    # Create a circle to use for the Gaze Cursor. Current units assume pix.
    #
    gaze_dot = visual.GratingStim(window, tex=None, mask="gauss", pos=(0, 0),
                                  size=(66, 66), color='green', units=coord_type)

    # Create a Text Stim for use on /instruction/ type screens.
    # Current units assume pix.
    instructions_text_stim = visual.TextStim(window, text='', pos=[0, 0], height=24, color=[-1, -1, -1],
                                             colorSpace='rgb', wrapWidth=window.size[0]*.9)

    # Update Instruction Text and display on screen.
    # Send Message to ioHub DataStore with Exp. Start Screen display time.
    #
    instuction_text = "Press Any Key to Start Experiment."
    instructions_text_stim.setText(instuction_text)
    instructions_text_stim.draw()
    flip_time = window.flip()
    io_hub.sendMessageEvent(text="EXPERIMENT_START", sec_time=flip_time)

    # Wait until a key event occurs after the instructions are displayed
    io_hub.clearEvents('all')
    kb.waitForPresses()

    # Send some information to the ioDataStore as experiment messages,
    # including the experiment and session id's, the calculated pixels per
    # degree, display resolution, etc.
    #
    io_hub.sendMessageEvent(text="IO_HUB EXPERIMENT_INFO START")
    io_hub.sendMessageEvent(text="ioHub Experiment started {0}".format(getCurrentDateTimeString()))
    io_hub.sendMessageEvent(text="Experiment ID: {0}, Session ID: {1}".format(io_hub.experimentID,
                                                                              io_hub.experimentSessionID))
    io_hub.sendMessageEvent(text="Stimulus Screen ID: {0}, "
                            "Size (pixels): {1}, CoordType: {2}".format(display.getIndex(),
                                                                        display.getPixelResolution(),
                                                                        display.getCoordinateType()))
    io_hub.sendMessageEvent(text="Calculated Pixels Per Degree: {0} x, {1} y".format(*display.getPixelsPerDegree()))
    io_hub.sendMessageEvent(text="IO_HUB EXPERIMENT_INFO END")

    io_hub.clearEvents('all')

    # For each trial in the set of trials within the current block.
    #
    t = 0
    for trial in trials:
        # Update the instruction screen text to indicate
        # a trial is about to start.
        #
        instuction_text = "Press Space Key To Start Trial %d" % t
        instructions_text_stim.setText(instuction_text)
        instructions_text_stim.draw()
        flip_time = window.flip()
        io_hub.sendMessageEvent(text="EXPERIMENT_START", sec_time=flip_time)

        # Wait until a space key press event occurs after the
        # start trial instuctions have been displayed.
        #
        io_hub.clearEvents('all')
        kb.waitForPresses(keys=[' ', ])

        # Space Key has been pressed, start the trial.
        # Set the current session and trial id values to be saved
        # in the ioDataStore for the upcoming trial.
        #

        trial['session_id'] = io_hub.getSessionID()
        trial['trial_id'] = t+1

        # Send a msg to the ioHub indicating that the trial started, and the time of
        # the first retrace displaying the trial stm.
        #
        io_hub.sendMessageEvent(text="TRIAL_START", sec_time=flip_time)

        # Start Recording Eye Data
        #
        tracker.setRecordingState(True)

        # Get the image stim for this trial.
        #
        imageStim = image_cache[trial['IMAGE_NAME']]
        imageStim.draw()
        flip_time = window.flip()
        # Clear all the events received prior to the trial start.
        #
        io_hub.clearEvents('all')
        # Send a msg to the ioHub indicating that the trial started,
        # and the time of the first retrace displaying the trial stim.
        #
        io_hub.sendMessageEvent(text="TRIAL_START", sec_time=flip_time)
        # Set the value of the trial start variable for this trial
        #
        trial['TRIAL_START'] = flip_time

        # Loop until we get a keyboard event
        #
        run_trial = True
        while run_trial is True:
            # Get the latest gaze position in display coord space..
            #
            gpos = tracker.getPosition()
            if type(gpos) in [tuple, list]:
                # If we have a gaze position from the tracker,
                # redraw the background image and then the
                # gaze_cursor at the current eye position.
                #
                gaze_dot.setPos([gpos[0], gpos[1]])
                imageStim.draw()
                gaze_dot.draw()
            else:
                # Otherwise just draw the background image.
                # This will remove the gaze cursor from the screen
                # when the eye tracker is not successfully
                # tracking eye position.
                #
                imageStim.draw()

            # Flip video buffers, displaying the stim we just
            # updated.
            #
            flip_time = window.flip()

            # Send an experiment message to the ioDataStore
            # indicating the time the image was drawn and
            # current position of gaze spot.
            #
            if type(gpos) in [tuple, list]:
                io_hub.sendMessageEvent("IMAGE_UPDATE %s %.3f %.3f" % (trial['IMAGE_NAME'], gpos[0], gpos[1]),
                                        sec_time=flip_time)
            else:
                io_hub.sendMessageEvent("IMAGE_UPDATE %s [NO GAZE]" % (trial['IMAGE_NAME']),
                                        sec_time=flip_time)

            # Check any new keyboard press events by a space key.
            # If one is found, set the trial end variable and break.
            # from the loop
            if kb.getPresses(keys=[' ', ]):
                run_trial = False
                break

        # The trial has ended, so update the trial end time condition value,
        # and send a message to the ioDataStore with the trial end time.
        #
        flip_time = window.flip()
        trial['TRIAL_END'] = flip_time
        io_hub.sendMessageEvent(text="TRIAL_END %d" % t, sec_time=flip_time)

        # Stop recording eye data.
        # In this example, we have no use for any eye data
        # between trials, so why save it.
        #
        tracker.setRecordingState(False)

        # Save the experiment condition variable values for this
        # trial to the ioDataStore.
        #
        io_hub.addTrialHandlerRecord(trial)

        # Clear all event buffers
        #
        io_hub.clearEvents('all')
        t += 1

    # All trials have been run, so end the experiment.
    #

    flip_time = window.flip()
    io_hub.sendMessageEvent(text='EXPERIMENT_COMPLETE', sec_time=flip_time)

    # Disconnect the eye tracking device.
    #
    tracker.setConnectionState(False)

    # The experiment is done, all trials have been run.
    # Clear the screen and show an 'experiment  done' message using the
    # instructionScreen text.
    #
    instuction_text = "Press Any Key to Exit Demo"
    instructions_text_stim.setText(instuction_text)
    instructions_text_stim.draw()
    flip_time = window.flip()
    io_hub.sendMessageEvent(text="SHOW_DONE_TEXT", sec_time=flip_time)
    io_hub.clearEvents('all')
    # wait until any key is pressed
    kb.waitForPresses()
