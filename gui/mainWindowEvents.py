
import wx

EVT_LOGAVAIL_ID = wx.NewId()
EVT_LOGGED_ID = wx.NewId()
EVT_ENABLE_ID = wx.NewId()
EVT_ENABLE_STOP_ID = wx.NewId()
EVT_SETRUN_ID = wx.NewId()
EVT_SETFAILED_ID = wx.NewId()
EVT_FAILUREADD_ID = wx.NewId()
EVT_SUCCESSADD_ID = wx.NewId()
EVT_FAILURERESET_ID = wx.NewId()
EVT_SUCCESSRESET_ID = wx.NewId()
EVT_CURRENTSCRIPT_ID = wx.NewId()
EVT_UPDATETIME_ID = wx.NewId()
EVT_CURRENTSTEP_ID = wx.NewId()
EVT_TOTALSTEPS_ID = wx.NewId()
EVT_MANUALCHECK_ID = wx.NewId()
EVT_LOADATEFILE_ID = wx.NewId()
EVT_RUNASE_ID = wx.NewId()
EVT_CLOSEAPP_ID = wx.NewId()
EVT_TOTALSCRIPTS_ID = wx.NewId()
EVT_CONNECTIONLOST_ID = wx.NewId()
EVT_RIGHTBUTTON_ENABLE = wx.NewId()
EVT_RIGHTBUTTON_DISABLE = wx.NewId()
EVT_PROJSELECT_ENABLE = wx.NewId()

#################
# EVENT CLASSES #
#################

class RunEvent (wx.PyEvent):
    """Run Event
    @summary:
    Simple event to Run set of loaded script in ATE.
    Used for invoking ATE command line
    """
    def __init__ (self):
        """Init Result Event."""
        wx.PyEvent.__init__ (self)
        self.SetEventType (EVT_RUNASE_ID)
class CloseATEEvent (wx.PyEvent):
    """Close ATE Event
    @summary:
    Simple event to Close the ATE application
    Used for invoking ATE command line
    """
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CLOSEAPP_ID)
class LoadATEFileEvent (wx.PyEvent):
    """Load ATE File Event
    @summary:
    Simple event to load an ATE file.
    Used for invoking ATE command line
    """
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LOADATEFILE_ID)
        self.data = data

class AddFailureEvent(wx.PyEvent):
    """Add Failure Event
    @summary:
    Simple event to add a failure to the display."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_FAILUREADD_ID)

class AddSuccessEvent(wx.PyEvent):
    """Add Success event
    @summary:
    Raised whenever the currently being run test succeeds one of its steps.
    Upon receiving that event, the HMI updates the fail / success counters
    displayed
    """
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SUCCESSADD_ID)

class ResetFailuresEvent(wx.PyEvent):
    """Reset Failures event
    @summary:
    Raised whenever we want to reset the failure counter on the HMI.
    Upon receiving that event, the HMI resets the fail counter displayed
    """
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_FAILURERESET_ID)

class ResetSuccessEvent(wx.PyEvent):
    """Reset Success event
    @summary:
    Raised whenever we want to reset the success counter on the HMI.
    Upon receiving that event, the HMI resets the success counter displayed
    """
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SUCCESSRESET_ID)

class CurrentScriptEvent (wx.PyEvent):
    """Current Step event
    @summary:
    Raised whenever we want to update the progress bar consequently
    to a new script being complete.
    """
    def __init__(self, current):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self._current = current
        self.SetEventType (EVT_CURRENTSCRIPT_ID)

class TotalScriptsEvent (wx.PyEvent):
    """Current Step event
    @summary:
    Raised whenever we want to update the progress bar consequently
    to a new script count being reached.
    """
    def __init__(self, totalScripts):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self._total = totalScripts
        self.SetEventType (EVT_TOTALSCRIPTS_ID)

class TotalStepsEvent (wx.PyEvent):
    """Current Step event
    @summary:
    Raised whenever we want to update the progress bar consequently
    to a new step being reached in a test script.
    """
    def __init__(self, totalSteps):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self._total = totalSteps
        self.SetEventType(EVT_TOTALSTEPS_ID)

class CurrentStepEvent(wx.PyEvent):
    """Current Step event
    @summary:
    Raised whenever we want to update the progress bar consequently
    to a new step being reached in a test script.
    """
    def __init__(self,current):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self._current = current
        self.SetEventType(EVT_CURRENTSTEP_ID)

class UpdateTimeEvent(wx.PyEvent):
    """Reset Success event
    @summary:
    Raised whenever we want to reset the success counter on the HMI.
    Upon receiving that event, the HMI resets the success counter displayed
    """
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATETIME_ID)

class LogAvailableEvent(wx.PyEvent):
    """Log Available Event
    @summary:
    Simple event to refresh the log window when stdout receives data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LOGAVAIL_ID)
        self.data = data

class TextLoggedAvailableEvent(wx.PyEvent):
    """Text Logged Available Event
    @summary:
    Simple event to refresh the log window when some log info has already been
    logged but not displayed to the screen
    """
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LOGGED_ID)
        self.data = data

class SetRunEvent(wx.PyEvent):
    """Clear Run Event
    @summary:
    Simple event to clear all run status from selected scripts."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SETRUN_ID)
        self.data = data

class ManualCheckEvent(wx.PyEvent):
    """Manual Check Event
    @summary:
    Event used to post a message requiring the UI to display a dialog
    and wait for the user to press yes or no
    """
    def __init__(self, text,queue):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_MANUALCHECK_ID)
        self.text = text
        self.queue = queue

class SetFailedEvent(wx.PyEvent):
    """Clear Run Event
    @summary:
    Simple event to clear all run status from selected scripts."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_SETFAILED_ID)
        self.data = data

class EnableStopButtonEvent(wx.PyEvent):
    """Enable Run Button Event
    @summary:
    Simple event to enable the run button after running some tests."""
    def __init__(self,value):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self._value = value
        self.SetEventType(EVT_ENABLE_STOP_ID)

class EnableRunButtonEvent(wx.PyEvent):
    """Enable Run Button Event
    @summary:
    Simple event to enable the run button after running some tests."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_ENABLE_ID)

class DisableRTDSConnectionEvent(wx.PyEvent):
    def __init__(self, value):
        wx.PyEvent.__init__(self)
        self.value = value
        self.SetEventType(EVT_CONNECTIONLOST_ID)
        
class DisableRightButton(wx.PyEvent):
    """Disable right Button Event
    @summary:
    Simple event to disable the right button after running some tests."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RIGHTBUTTON_DISABLE)
        
class EnableRightButton(wx.PyEvent):
    """Enable right Button Event
    @summary:
    Simple event to enable the right button after running some tests."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RIGHTBUTTON_ENABLE)

class EnableProjectSelect(wx.PyEvent):
    """Enable project select
    @summary:
    Simple event to enable the project select after running some tests."""
    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PROJSELECT_ENABLE)
