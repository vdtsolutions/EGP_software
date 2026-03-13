"""
==============================================================
LoaderDialog + Worker Integration Guide
==============================================================

LoaderDialog is a generic progress UI used for long-running
operations (line chart, heatmap, reports, etc.).

Workers must communicate with LoaderDialog using signals
defined in BaseWorker.

--------------------------------------------------------------
Signals LoaderDialog listens to
--------------------------------------------------------------

progress(int)
    Updates the progress bar.

    Example:
        self.progress.emit(40)

message(str)
    Updates the status label in the loader.

    Example:
        self.message.emit("Fetching data from GCP...")

finished(object)
    Signals that the worker has completed its task and returns
    the result to the UI.

    Example:
        self.finished.emit(dataframe)

--------------------------------------------------------------
Typical worker execution flow
--------------------------------------------------------------

Workers should follow this structure inside run():

    1. Check cancellation
    2. Emit progress + status updates
    3. Perform heavy work
    4. Emit final result

Example:

    def run(self):

        if self.isInterruptionRequested():
            return

        self.smooth_progress(0, 20, "Checking inputs...")

        if self.isInterruptionRequested():
            return

        data = fetch_data()

        self.smooth_progress(80, 95, "Preparing chart...")

        self.finished.emit(data)

--------------------------------------------------------------
Cancellation support
--------------------------------------------------------------

LoaderDialog has a Cancel button.

Cancel triggers:

    worker.stop()

Which internally calls:

    requestInterruption()

Workers must periodically check:

    if self.isInterruptionRequested():
        return

This ensures tasks stop safely.

--------------------------------------------------------------
LoaderDialog UI methods
--------------------------------------------------------------

Workers do NOT call these directly.
They are triggered via signals.

update_progress(value)
update_status(text)

--------------------------------------------------------------
Lifecycle
--------------------------------------------------------------

User clicks button
        ↓
LoaderDialog opens
        ↓
Worker thread starts
        ↓
Worker emits progress + message
        ↓
LoaderDialog updates UI
        ↓
Worker emits finished(data)
        ↓
UI renders output
        ↓
LoaderDialog closes

--------------------------------------------------------------
Important rules
--------------------------------------------------------------

✔ Workers must emit progress updates
✔ Workers must emit status messages
✔ Workers must emit finished(result)
✔ Workers must check interruption
✔ Workers must NOT update UI directly

All UI updates happen through signals.

==============================================================
"""

#you need to create a clss which will inherit baseworker already present in loader_dialog
#you also need to connect loaderdialog class from the class which is runnning the dialog
# the run function runs inside the thread (run from worker class)
#the ui runs on main thread