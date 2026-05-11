"""
Fusion script template.

Purpose:
- Provide a safe starting point for Fusion API scripts.

Tested with:
- Autodesk Fusion API (Python)

Notes:
- Duplicate this file and rename to fusion-[purpose].py
- Register UI objects in run() and clean them in stop()
"""

import traceback

# Fusion API imports are intentionally local to keep linting simple on machines
# without Fusion installed.
import adsk.core
import adsk.fusion
import adsk.cam

APP = None
UI = None


def run(context):
    global APP, UI

    try:
        APP = adsk.core.Application.get()
        UI = APP.userInterface

        UI.messageBox("Fusion script template loaded. Replace this message with your logic.")

    except Exception:
        if UI:
            UI.messageBox("run() failed:\n{}".format(traceback.format_exc()))


def stop(context):
    try:
        # Add cleanup logic for command definitions, handlers, and panels here.
        pass

    except Exception:
        if UI:
            UI.messageBox("stop() failed:\n{}".format(traceback.format_exc()))
