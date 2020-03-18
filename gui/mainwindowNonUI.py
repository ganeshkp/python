
import wx
from mainWindowEvents import *
import threading
from time import sleep

class CFATMainWindowNonUI ():
    """CFATMainWindowNonUI
    @summary:
    Main window non UI related functionality of the Automated Scripting Environment
    """
    _instance = None
    @staticmethod
    def getInstance():
        """Get Instance
        @summary:
        Allows getting the instance of this class if any, to use it as a
        singleton. This is a convenience to avoid having to inform all the
        users when / if it was created. So this class should be instanciated
        once in the application life and then if any call as to be done, the
        instance reference can be obtained by calling this function.
        @return: singleton instance of the class to avoid having more than one.
        """
        return CFATMainWindowNonUI._instance    
    
    def __init__(self, mainThreadId):
        """__init__
        @summary: constructor of the class CFATMainWindowNonUI
        @param mainThreadId: main thread identifier
        @return: None
        """
        self.uiThread = mainThreadId
        if CFATMainWindowNonUI._instance:
            raise Exception("There is already a mainwindowNonUI instance" \
                "Please use CFATMainWindowNonUI.getInstance() to get it")
        CFATMainWindowNonUI._instance = self

    def checkUIThread (self):
        """checkUIThread
        @summary: Checks we are called from the UI thread
        @raise: Exception if called from a non UI thread
        @note: Can only be called by the main application's thread
        @return: None
        """
        if not self.uiThread == threading.current_thread().ident:
            raise Exception ("UI method called from a non UI thread")

    def triggerASEClose(self):
        """triggerASEClose
        @summary:
        Raise an event to close the application from the main app thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, CloseATEEvent())

    def triggerSetRun (self, testName):
        """triggerSetRun
        @summary:
        Sets the run status of given script
        Called when a python test script has been run
        @param testName: name of the script
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, SetRunEvent (testName))

    def triggerLogAvailable (self, logstr):
        """triggerLogAvailable
        @summary: Tells the UI a log is available to be displayed
        @param logstr: log line to be displayed
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, TextLoggedAvailableEvent(logstr))

    def triggerSetFailed (self, testName):
        """trigger set failed
        @summary: 
        Sets a script as failed so it becomes red on the selected
        Scripts widget
        Called when the python test scripts are finished
        @param testName: name of the failed test 
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, SetFailedEvent (testName))
    
    def triggerConnectionLostEvent (self,value):
        """trigger connection lost
        @summary: 
        called when connection is lost
        @param value: value  
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, DisableRTDSConnectionEvent(value))
        
    def testFinished (self):
        """testFinished
        @summary: Function to be called when the current test is finished to
        update the HMI accordingly
        @note: Can be called from any thread
        @return: None
        """
        self.enableRunButton()
        self.triggerEnableStopButton(False)

        
    def triggerTotalSteps (self, totalSteps):
        """trigger Total Steps
        @summary: posts the TotalStepsEvent so wx calls the updateTotalSteps
        function in the main thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, TotalStepsEvent(totalSteps))

    def triggerCurrentStep(self, current):
        """triggerCurrentStep
        @summary: posts the CurrentStepEvent so wx calls the updateCurrentStep
        function in the main thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, CurrentStepEvent(current))

    def triggerCurrentScript (self, current):
        """triggerCurrentStep
        @summary: posts the CurrentStepEvent so wx calls the
        updateCurrentScript function in the main thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, CurrentScriptEvent (current))

    def triggerTotalScripts (self, total):
        """triggerCurrentStep
        @summary: posts the TotalStepEvent so wx calls the
        updateTotalScript function in the main thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, TotalScriptsEvent (total))

    def triggerUpdateTime (self):
        """triggerUpdateTime
        @summary: posts the UpdateTimeEvent so wx calls the updateTestTime
        function in the main thread
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, UpdateTimeEvent())

    def updateTimeThread (self, args):
        """updateTimeThread
        @summary: This function is called in a separate thread to care of
        the timer update
        @note:
        Woken every second to update the timer
        @param args: unused list of arguments 
        @return: None
        """
        while True:
            sleep(1)
            if self.closing:
                return
            wx.PostEvent (self, UpdateTimeEvent())
            
    def triggerAddSuccess (self):
        """triggerAddSuccess
        @summary: posts an event to the main application thread so a success is
        added to the HMI display for the test being currently run
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, AddSuccessEvent ())

    def triggerAddFailure (self):
        """triggerAddFailure
        @summary: posts an event to the main application thread so a failure is
        added to the HMI display for the test being currently run
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, AddFailureEvent ())

    def triggerResetSuccesses(self):
        """triggerResetSuccesses
        @summary: Will send a message to the main thread so it resets the 
        successes count to zero
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, ResetSuccessEvent())

    def triggerResetFailures(self):
        """triggerResetFailures
        @summary: For the running test, the HMI displays the number of
        fails / successes.
        This function will send a message to the main thread so it resets the 
        failures count to zero
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, ResetFailuresEvent())
        
    def openLogThread (self, log):
        """openLogThread
        @summary: Opens and displays the log contents in a notepad
        @param log: full or relative path of the log file
        @return: None
        """
        command = "notepad %s"%log
        from subprocess import call
        call(command, shell=True)
        
    def getProjectSpecificsInstance (self):
        """getProjectSpecificsInstance
        @summary: ATE can be used on many projects.
        Each projects has a specific set of settings.
        This function is a getter allowing to access the model class that
        allows accessing those project specific settings
        (class:projectSpecifics)
        @note: Can be called from any thread
        @return: singleton instance of the project specifics model
        (class:projectSpecifics)
        """
        from projectSpecificsModel import ProjectSpecificsModel
        psInstance = ProjectSpecificsModel.getInstance ()
        return psInstance
    
    def enableRunButton (self):
        """Enable the run button
        @summary: Called when the python test scripts are finished
        @note: Can be called from any thread
        @return: None
        """
        wx.PostEvent (self, EnableRunButtonEvent())
        
    def triggerRunEvent (self):
        """raise Run ATE event
        @summary:Asks for the run button to be pressed in the main UI thread 
        @return: None
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        """
        wx.PostEvent (self, RunEvent())
        
    def shouldQuitWhenDone (self):
        """quit when done
        @summary: 
        Asks ATE to stop after the current test is finished
        @note: It is safe to call this
               function from any thread
        @return: None
        """
        self.quitWhenDone = True
        
    def triggerLoadATEFileEvent (self, loadPath):
        """raise load ATE File event
        @summary: Asks for the UI thread to load an ATE file
        @return: None
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        """
        wx.PostEvent (self, LoadATEFileEvent(loadPath))
        
    def setDummySession (self, dummy):
        """set dummy session
        @summary: Sets if this session is a dummy or a real one
        (debug session or actual test on the kit)
        @param dummy: True if debugging
                      False if on the kit
        @return: None
        """
        self._dummySession=dummy
    def getDummySession (self):
        """get dummy session
        @summary: Tells if this session is a dummy or a real one
        @return: True if debugging
                 False if on the kit
        """
        return self._dummySession
    dummySession=property(getDummySession,setDummySession)

    def setHeader (self, header):
        """Set the header
        @summary: The header is used when saving test logs, it contains the
        software version information gathered by the Software Version
        Information window
        @param header: new header to be set (text)
                       header will be displayed at the start of the test 
        @return: None
        """
        self._header = header
    def getHeader (self):
        """Get the header
        @summary: The header is used when saving test logs, it contains the
        software version information gathered by the Software Version
        Information window
        @return: the header (text)
        """
        return self._header
    header = property(getHeader,setHeader)
    
    def ManualCheck (self, text):
        """ ManualCheck
        @summary: Function used by tests to perform a manual check, i.e. will
        prompt the user and ask him to check manually something on the kit
        As the test is not in the application main thread, this function will
        post an event so the job is done in the main thread and wait until the
        main thread posts the result in a wait queue  
        @note: This function must be called from another thread
               not from the main UI thread
               From the main UI thread call manualCheckHandler instead
        @return: result of the manual checking (usually wx.ID_YES or wx.ID_NO) 
        """
        #Create a wait queue to synch this thread with the main UI one
        waitQueue = Queue.Queue()
        #Post an event in the main UI thread to ask for the user's input
        wx.PostEvent (self, ManualCheckEvent(text,waitQueue))
        #Wait for that input to be filled
        result = waitQueue.get()
        #Close the queue
        waitQueue.task_done()
        return result

    def getParams (self):
        """getParams
        @summary: Gets the whole list of non project specific parameters
        @note: Can only be called from the main UI thread
        @return: dictionary of parameters, the param name is the key
                 the value is the param's value
        """
        paramlist = self.runConfigWindow.getParams()
        paramlist["DUMMY_SESSION"]=self.dummySession
        paramlist["HEADER"]=self.header
        apexContextPath = self._apexCfg.GetValue()
        if apexContextPath == "":
            apexContextPath = None
        paramlist["APEX_CONTEXT_PATH"]=apexContextPath
        paramlist["RTDS_INSTANCE"]=self.rtds
        if self.logFolder:
            paramlist["EXTRACT_PATH"]=self.logFolder
        if self.loadRTDS:
            paramlist['LOAD_RTDSMODEL_FROM_SVN'] = self.loadRTDS
        if self.svnUserName:
            paramlist['RTDS_SVN_USERNAME'] = self.svnUserName
        if self.svnPassword:
            paramlist['RTDS_SVN_PASSWORD'] = self.svnPassword
        return paramlist
    params=property(getParams)

    def triggerEnableStopButton (self, value):
        """Enable the stop button
        @summary:
        Called when the python test scripts are finished / starting
        Can be called from any thread
        @param value: boolean
                      False to disable
                      True to enable
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, EnableStopButtonEvent(value))

    def postLog (self, text):
        """Post log
        @summary:
        Function than can be called outside the main window's applicative thread
        to add a message into the log widget
        @param text: text to display, will be displayed as it, no newline
                     will be added
        @return: None
        """
        wx.PostEvent (self, LogAvailableEvent (text))

    def setLogger (self, logger):
        """set logger
        @summary: Sets the logger for the main application thread
        @param logger: instance of logger class to be used as the main
        thread's logger 
        @return: None
        """
        self._logger = logger

    def getLogger(self):
        """get logger
        @summary: returns a reference to the main application thread's logger
        @return: logger reference (class:logger)
        """
        return self._logger
    logger = property(getLogger,setLogger)
    
    def manualCheckHandler (self, event):
        """manual Check Handler
        @summary: Function used by tests to perform a manual check, i.e. will
        prompt the user and ask him to check manually something on the kit
        As the test is not in the application main thread, the test will
        post an event so the job is done in the main thread by this function and
        the test will wait until this function posts the result in a wait queue  
        @note: This function must be called from another thread
               not from the main UI thread
               From the main UI thread call manualCheckHandler instead
        @param event: wx event unused parameter
                      required in all wx event handlers
        @param event.text question to be displayed into the dialog
        @param event.queue message queue used to post the result
        @return: None (a message queue is used for the result as it will be
        read by another thread)
        """
        #mydlg=wx.MessageDialog(None, event.text, "Manual Verification", \
        #                       wx.YES_NO | wx.ICON_INFORMATION)
        mydlg=ManualVerificationDialog (self, event.text, "Manual Verification")
        returnValue = mydlg.showModal ()
        event.queue.put(returnValue)
        event.queue.join()
        
    def triggerEnableRightButton (self):
        """Enable right button
        @summary:
        Called when the python test scripts are finished / starting
        Can be called from any thread
        @param value: boolean
                      False to disable
                      True to enable
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, EnableRightButton())
        
    def triggerEnableProjectSelect (self):
        """Enable Project select 
        @summary:
        Called when the python test scripts are finished / starting
        Can be called from any thread
        @param value: boolean
                      False to disable
                      True to enable
        @note: Can be called from any thread
               UI can only be called by the UI thread
               this is the reason why the code is not done here
               But instead an event is triggered asking for the UI thread
               to do the job
        @return: None
        """
        wx.PostEvent (self, EnableProjectSelect())