
import sys
import datetime
from os import listdir
import threading
from Test_gct import gct_select

# ATE currently uses python 3.4, those few lines here were inserted to ensure
# We still are compatible with python 2.7
# We might not be 2.7 compatible anymore though, this needs to be assessed
try:
    #python 2.7
    import thread
    import Queue
except ImportError:
    #python 3.xx
    import _thread as thread
    import queue as Queue

from time import sleep
from genericpath import exists
from mainwindowNonUI import CFATMainWindowNonUI


_SPACING=6
_DEFAULT_WIDTH=1280
_DEFAULT_HEIGHT=600
_MIN_WIDTH=800
_MIN_HEIGHT=400
_CONFIG_WIDTH=700
_CONFIG_HEIGHT=440
_PS_WIDTH=450
_PS_HEIGHT=200
_RUNCONFIG_WIDTH=350
_RUNCONFIG_HEIGHT=300
_AUTO_RESIZE=0
_SELECTED_PANEL_WIDTH=250
_SELECTED_PANEL_HEIGHT=600

from mainWindowEvents import *

class DummyLogger():
    """Minimalist class to emulate a logger
    """
    def __init__ (self, mainWindow):
        self._mainW = mainWindow
    def println(self, line):
        self._mainW.postLog (line)

class CFATMainWindow (wx.Frame, CFATMainWindowNonUI):
    """CFATMainWindow
    @summary:
    Main window of the Automated Scripting Environment
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
        return CFATMainWindow._instance
    
    def __init__(self, parent, title, logFolder=None, svnUserName = None, svnPassword = None):
       
        
        """__init__
         @summary: constructor of the main window's class
         will populate the window with its widgets and set the events chains

         @param parent: parent function for the CFATMainWindow class
        
         @param title: Title of the ATE Tool to be displayed in ATE Window

         @param svnUserName:
         @param svnPassword:
         Additional option to sepcify SVN Credentials, which shall then be used
         by the ATE tool for SVN access 

         @return: None
        """
        # Note the ui THREAD id
        CFATMainWindowNonUI.__init__(self, 
                    mainThreadId = threading.current_thread().ident)

        self._totalScripts = 0
        self._currentScript = 0
        self.svnUserName = svnUserName
        self.svnPassword = svnPassword
        self.quitWhenDone = False
        self.logger = None
        self.rtds=None
        self.closing = False
        self._previouspath = None
        self._previousSP = None
        self.commandGeneratorWindow = None
        self._currentScriptsFolder = ""
        self._projectScriptsFolder = None
        self.requirementsDialog = None
        self.saveMenuItem = None
        self.loadPath = None
        self._script_source_dnd = ""
        self.uiThread = threading.current_thread().ident

        if CFATMainWindow._instance:
            raise Exception("There is already a mainwindow instance" \
                "Please use CFATMainWindow.getInstance() to get it")
        CFATMainWindow._instance = self
        self._app = wx.App (False)
        # Save stdout and redirect it to our log file
        self.saveout = sys.stdout
        wx.Frame.__init__(self, parent, title=title,
            size=(_DEFAULT_WIDTH,_DEFAULT_HEIGHT))
        self.fillTopMenu()
        favicon = wx.Icon('gct.ico',
                           wx.BITMAP_TYPE_ICO)
        self.SetIcon(favicon)
        # Bottom Statusbar
        self.CreateStatusBar ()

        #Contents of the window itself
        self._centerPanel = wx.Panel (self,-1)

        #Add the bottom elements (Scripts list + log zone)
        bottomPanel = wx.Panel (self._centerPanel)

        self.fillBottomThreePanels(bottomPanel)

        #Add the Panels vertically into the main panel
        self._vboxSizer = wx.BoxSizer(wx.VERTICAL)
        self._vboxSizer.AddSpacer(_SPACING)
        self._vboxSizer.Add (bottomPanel, proportion=1, flag=wx.EXPAND)
        self._vboxSizer.AddSpacer(_SPACING)
        self._centerPanel.SetSizer(self._vboxSizer)
        self.Connect(-1, -1, EVT_ENABLE_ID, self.enableRun)
        self.Connect(-1, -1, EVT_RUNASE_ID, self.onRun)
        self.Connect(-1, -1, EVT_CLOSEAPP_ID, self.onExitNoQuestion)

        self.header=""
        # Show the main window
        self.Show(True)
        # Now we can start listening to stdout
        self.startListeningLog()
        self.SetMinSize((_MIN_WIDTH,_MIN_HEIGHT))

    ################################
    # SELECTED SCRIPTS WIDGET CODE #
    # http://wxpython.org/Phoenix/docs/html/TreeCtrl.html #
    ################################


    def clearSelected (self):
        # OK
        """clear selected
        @summary: Removes all items from the selected scripts' list
        @note: should be called from the main UI thread
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        self._selectedListBox.DeleteAllItems()
        #Need to recreate columns and all
        self.initSelectedWidget ()

    ################################
    # SELECTED SCRIPTS WIDGET CODE #
    ################################
    def addLogPanel (self, parent):
        """Create Log panel
        @summary:
        Fills the widget contained in the rightmost part of the window
        Start, stop, clear log, save log and RTDS buttons
        @note: needs to be called from the application main thread. Ideally
        called by this class's constructor
        @param parent: parent widget where to create all these widgets 
        @return: None
        """
        self.checkUIThread()
        if _AUTO_RESIZE:
            logPanel = wx.Panel(parent)
        else:
            logPanel = wx.Panel(parent,size=wx.Size(50,150))
        logVboxSizer = wx.BoxSizer(wx.VERTICAL)
        logTopPanel = wx.Panel(logPanel)

        #Script being run
        runningLabel = wx.StaticText (logTopPanel,-1, \
            "EXECUTION LOG")

        #Add all labels to the layout
        labelsHboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelsHboxSizer.AddStretchSpacer()
        labelsHboxSizer.Add (runningLabel, proportion = 0, \
            flag=wx.EXPAND)
        labelsHboxSizer.AddStretchSpacer()
        labelsHboxSizer.AddSpacer (_SPACING*5)
        labelsHboxSizer.AddSpacer (_SPACING*5)
        logTopPanel.SetSizer (labelsHboxSizer)

        #Buttons
        buttonsPanel = wx.Panel (logPanel)

        #Run button creation and link to event function
        bmpRun = wx.Bitmap("doc/run.png", wx.BITMAP_TYPE_ANY)
        self._runButton = wx.BitmapButton ( \
            buttonsPanel, id=wx.ID_FORWARD, bitmap=bmpRun, \
            size=(bmpRun.GetWidth()+10, bmpRun.GetHeight()+10))
        self._runButton.SetToolTip(wx.ToolTip( \
            "Run currently selected set of scripts"))
        self.Bind(wx.EVT_BUTTON, self.onRun, self._runButton)

        #Clear button creation and link to event function
        bmpClearLog = wx.Bitmap("doc/clear_log.png", wx.BITMAP_TYPE_ANY)
        self._clearButton = wx.BitmapButton ( \
            buttonsPanel, id=wx.ID_CLEAR, bitmap=bmpClearLog, \
            size=(bmpClearLog.GetWidth()+10, bmpClearLog.GetHeight()+10))
        self._clearButton.SetToolTip(wx.ToolTip( \
            "Clear the log window\n" \
            "The log files will not be erased"))
        self.Bind(wx.EVT_BUTTON, self.onClear, self._clearButton)

        #Save button creation and link to event function
        bmpSaveLog = wx.Bitmap("doc/floppy.png", wx.BITMAP_TYPE_ANY)
        saveLogButton = wx.BitmapButton ( \
            buttonsPanel, id=wx.ID_SAVEAS, bitmap=bmpSaveLog, \
            size=(bmpSaveLog.GetWidth()+10, bmpSaveLog.GetHeight()+10))
        saveLogButton.SetToolTip(wx.ToolTip( \
            "Save the content of the log window"))
        self.Bind(wx.EVT_BUTTON, self.onSaveLog, saveLogButton)

        """#RTDS connect button
        self._bmpRTDSDisconnected = wx.Bitmap ( \
            "doc/disconnected.png", wx.BITMAP_TYPE_ANY)
        self._bmpRTDSConnected = wx.Bitmap( \
            "doc/connected.png", wx.BITMAP_TYPE_ANY)
        self._rtdsButton = wx.BitmapButton ( \
            buttonsPanel, id=wx.ID_ANY, bitmap=self._bmpRTDSDisconnected, \
            size=(self._bmpRTDSDisconnected.GetWidth()+10, \
                  self._bmpRTDSDisconnected.GetHeight()+10))
        self._rtdsButton.SetToolTip ( \
            wx.ToolTip("RTDS connection\nRED:disconnected GREEN:connected"))
        self.Bind (wx.EVT_BUTTON, self.onRTDSConnect, self._rtdsButton)"""

        #Log widget
        self._logBox = wx.TextCtrl(logPanel, \
            style=wx.TE_MULTILINE|wx.TE_READONLY)
        fontCourrier = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, \
                               False, u'Courrier')
        self._logBox.SetFont(fontCourrier)

        progressBarsPanel = wx.Panel(buttonsPanel)
        self._testProgressBar = wx.Gauge (
            progressBarsPanel)

        progressBarsVboxSizer = wx.BoxSizer (wx.VERTICAL)
        progressBarsVboxSizer.Add (self._testProgressBar, proportion = 1,
            flag=wx.EXPAND)
        progressBarsPanel.SetSizer(progressBarsVboxSizer)

        # Add all this to the layout
        buttonsHboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsHboxSizer.Add(self._runButton, proportion=0,
            flag=wx.EXPAND)
        buttonsHboxSizer.Add(self._clearButton, proportion=0,
            flag=wx.EXPAND)
        buttonsHboxSizer.Add(saveLogButton, proportion=0,
            flag=wx.EXPAND)
        buttonsPanel.SetSizer(buttonsHboxSizer)

        logVboxSizer.Add(logTopPanel, proportion=0,
            flag=wx.EXPAND)
        logVboxSizer.Add(buttonsPanel, proportion=0,
            flag=wx.EXPAND)
        logVboxSizer.Add(self._logBox, proportion=1,
            flag=wx.EXPAND)
        logPanel.SetSizer(logVboxSizer)
        return logPanel


    def onSaveLog (self, event):
        """on save log
        @summary:
        Function called when the save log button is pressed
        Will save the contents of the log widget into a file.
        @note: Can only be called from the main UI thread
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        lines = self._logBox.GetValue()
        creationstring = datetime.datetime.today().strftime("%Y-%m-%d--%H%M%S")
        logfilename = "logs/logwindow_" + creationstring + ".log"
        logfile = open(logfilename, 'w+')
        for line in lines.split("\n"):
            logfile.write ("%s\n"%line)
        logfile.close()
        self.printLog("log saved as %s"%logfilename)

    def fillBottomThreePanels (self, parent):
        """fillBottomThreePanels
        @summary: Populates the central three panels with their widgets
        @param parent: parent widget where to create those three panels
        @note: Can only be called from the main UI thread
        @return: None 
        """
        self.checkUIThread()
        inpOutputSelPanel = self.selectInpOutPutPanel(parent)
        logPanel = self.addLogPanel(parent)
        
        #let the window handle the widgets' sizes
        #Add Script List and log panel in the bottom horizontally
        bottomHboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomHboxSizer.AddSpacer(_SPACING)
        bottomHboxSizer.Add(inpOutputSelPanel, proportion=0,
                                  flag=wx.EXPAND)
        bottomHboxSizer.AddSpacer(_SPACING)
        
        bottomHboxSizer.Add(logPanel, proportion=1,
                                  flag=wx.EXPAND)
        bottomHboxSizer.AddSpacer(_SPACING)
        parent.SetSizer(bottomHboxSizer)

    def OnScriptBeginDrag(self, event):
        """
        Event handler when mouse button is pressed during drag and drop.
        event.Allow() - need to be called to allow drag and drop.
        @argument: event - wx.NotifyEvent
        @return: None
        """
        event.Allow()
        self._script_source_dnd = event.GetItem()

    def move_tree_item(self, tree_instance, source, target):
        """
        Move wxtree item into a new position
        @argument: tree_instance - wx.TreeCtrl object
        @argument: source - tree item object - tree item that will be moved to a 
        target item of the tree
        @argument: target - tree item object - tree item to where source item
        will be moved
        return: None
        """
        tree_instance.AppendItem(target, tree_instance.GetItemText(source))
        tree_instance.Delete(source)

    def onConfigFileSelect(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, "Choose Config File", "", "", \
                                       "xml file (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print ("You chose the following file(s):")
            for path in paths:
                self._configFileSelectPath.SetValue(path)
        dlg.Destroy()
        
    def onComtradeFolderSelect(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self._comtradeFolderSelectPath.SetValue(dlg.GetPath())
        dlg.Destroy()
        
    def onOutputFolderSelect(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self._outputFolderSelectPath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def selectInpOutPutPanel (self, parent):
        """Add Script List Panel
        @summary: Fills the left list widget
        @param parent: widget to fill with the script panel widgets (a Panel)
        @note: Can only be called from the main UI thread
        @return: None
        """
        self.checkUIThread()
        #Script list panel
        scriptListVboxSizer = wx.BoxSizer(wx.VERTICAL)
        scriptListPanel = wx.Panel (parent, size = wx.Size (500, 250))
        scriptListLabel = wx.StaticText (scriptListPanel, -1, "INPUT/OUTPUT SELECTION", (100, 70), (160, -1), wx.ALIGN_CENTER)        
        
        # Create Configuration file selection button        
        configFilePanel = wx.Panel (scriptListPanel)
        nameLabel=wx.StaticText (configFilePanel,-1, "Configuration File(xml)")
        self._configFileSelectPath = wx.TextCtrl(configFilePanel, size = (300,50), style = wx.TE_MULTILINE | wx.TE_READONLY)
        bmpRight = wx.Bitmap ("doc/open.png", wx.BITMAP_TYPE_ANY)
        self._configRightButton = wx.BitmapButton ( \
            configFilePanel, id = wx.ID_ANY, bitmap=bmpRight, size=(20,20))
        self._configRightButton.SetToolTip ( \
            wx.ToolTip ('Select CFAT Configuration File(xml)'))
        self.Bind (wx.EVT_BUTTON, self.onConfigFileSelect, self._configRightButton)
        hboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hboxSizer.Add (nameLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        hboxSizer.Add (self._configFileSelectPath, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,10)
        hboxSizer.Add (self._configRightButton, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        configFilePanel.SetSizer (hboxSizer)
        
        # COMTRADE folder path selection button        
        comtradeFolderPanel = wx.Panel (scriptListPanel)
        nameLabel=wx.StaticText (comtradeFolderPanel,-1, "COMTRADE files folder")
        self._comtradeFolderSelectPath = wx.TextCtrl(comtradeFolderPanel, size = (300,50), style = wx.TE_MULTILINE | wx.TE_READONLY)
        bmpRight = wx.Bitmap ("doc/open.png", wx.BITMAP_TYPE_ANY)
        self._comtradeRightButton = wx.BitmapButton ( \
            comtradeFolderPanel, id = wx.ID_ANY, bitmap=bmpRight, size=(20,20))
        self._comtradeRightButton.SetToolTip ( \
            wx.ToolTip ('Select folder containing subfolders having COMTRADE files'))
        self.Bind (wx.EVT_BUTTON, self.onComtradeFolderSelect, self._comtradeRightButton)
        hboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hboxSizer.Add (nameLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        hboxSizer.Add (self._comtradeFolderSelectPath, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,10)
        hboxSizer.Add (self._comtradeRightButton, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        comtradeFolderPanel.SetSizer (hboxSizer)
        
        # Target output directory selection button        
        targetDirPanel = wx.Panel (scriptListPanel)
        nameLabel=wx.StaticText (targetDirPanel,-1, "Output Target Directory")
        self._outputFolderSelectPath = wx.TextCtrl(targetDirPanel, size = (300,50), style = wx.TE_MULTILINE | wx.TE_READONLY)
        bmpRight = wx.Bitmap ("doc/open.png", wx.BITMAP_TYPE_ANY)
        self._outputRightButton = wx.BitmapButton ( \
            targetDirPanel, id = wx.ID_ANY, bitmap=bmpRight, size=(20,20))
        self._outputRightButton.SetToolTip ( \
            wx.ToolTip ('Select folder containing subfolders having COMTRADE files'))
        self.Bind (wx.EVT_BUTTON, self.onOutputFolderSelect, self._outputRightButton)
        hboxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hboxSizer.Add (nameLabel, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        hboxSizer.Add (self._outputFolderSelectPath, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,10)
        hboxSizer.Add (self._outputRightButton, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        targetDirPanel.SetSizer (hboxSizer)

        
        scriptListVboxSizer.Add (scriptListLabel, proportion = 0, \
            flag=wx.EXPAND)
        scriptListVboxSizer.Add (configFilePanel, proportion = 0, \
            flag = wx.EXPAND)
        scriptListVboxSizer.Add (comtradeFolderPanel, proportion = 0, \
            flag = wx.EXPAND)
        scriptListVboxSizer.Add (targetDirPanel, proportion = 0, \
            flag = wx.EXPAND)
        scriptListPanel.SetSizer (scriptListVboxSizer)
        return scriptListPanel
       
    def isSaveButtonEnabled (self):
        """isSaveButtonEnabled
        @summary: Tells weither the save button is enabled or not
        @note: Can only be called from the main UI thread
        @return: True if the button is enabled
                 False if it not
        """
        self.checkUIThread()
        return self._saveSelectedButton.Enabled

    def enableSaveButton (self, enable = True):
        """enableSaveButton
        @summary: Enables / disables the save button on the HMI
        @note: Can only be called from the main UI thread
        @param enable: True to enable
                       False to disable 
        @return: None
        """
        self.checkUIThread()
        if enable:
            image = self._bmpSave
        else:
            image = self._bmpSaveGrayed
        self._bmpSaveGrayed = wx.Bitmap ( \
            "doc/floppy_grayed.png", wx.BITMAP_TYPE_ANY)
        self._saveSelectedButton.SetBitmapLabel(image)
        self._saveSelectedButton.Enable(enable)
    
    def enableSaveMenuItem (self, enable = True):
        """enableSaveMenuItem
        @summary: Enables / disables the save Menu Item on the HMI
        @note: Can only be called from the main UI thread
        @param enable: True to enable
                       False to disable 
        @return: None
        """
        self.checkUIThread()
        self.saveMenuItem.Enable(enable)

    def onChangeApexCfg (self, event):
        """on Change Apex Cfg
        @summary: Function called when the "ApEx Ctxt" button is clicked
        Will open a dialog to request which ApEx.ini file should be used when
        starting the ApEx.
        Once a file is selected, it will update the ApEx context control just
        above that button with the selected filename
        Whenever a test is run, this context will be used and the ApEx window
        will automatically be started / closed with the test
        @note: Can only be called from the main UI thread
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        dlg = wx.FileDialog (self,
            "Please Select Apex Context file",
            "C:\\ApEx","Apex.ini","*.ini")
        dlg.ShowModal()
        #fullPath = "%s\\%s"%(dlg.GetDirectory(),dlg.GetFilename())
        self._apexCfg.SetValue (dlg.GetFilename())
        del dlg

    def onSaveAsSelected (self, event):
        """on Save Selected
        @summary: Function called when the button with the save (floppy) icon
        is clicked, will request the filename from the user and then save the
        contents of the selected scripts list to the given file
        @note: should be called from the main UI thread
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        @see: loadATEFile
        """
        self.checkUIThread()
        fileName = "ATE_%s.ate"%datetime.date.today()
        dlg = wx.FileDialog (self,
            "Please Select File to save to",
            "",fileName,"*.ate",style=wx.FD_SAVE)
        dlg.ShowModal()
        savePath = "%s\\%s"%(dlg.GetDirectory(),dlg.GetFilename())
        del dlg
        self.saveToFile(savePath)
        
    def onSaveSelected (self, event):
        """on Save Selected
        @summary: Function called when the button with the save (floppy) icon
        is clicked, will request the filename from the user and then save the
        contents of the selected scripts list to the given file
        @note: should be called from the main UI thread
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        @see: loadATEFile
        """
        self.checkUIThread()
        if self.loadPath:
            savePath = self.loadPath
            self.saveToFile(savePath)
        else:
            self.onSaveAsSelected(event)

   
    def setUnmodified (self):
        """Set unmodified
        @summary: Sets the file as unmodified, this will disable saving it
        @note: Can only be called from the main UI thread
        @return: None
        """
        self.checkUIThread()
        self.enableSaveButton (False)
        self.enableSaveMenuItem (False)

    def setModified (self):
        """ser modified
        @summary: Sets the file as unmodified, this will enable saving it
        @note: Can only be called from the main UI thread
        @return: None
        """
        self.checkUIThread()
        self.enableSaveButton (True)
        self.enableSaveMenuItem (True)
    
    def onConfirm(self):
        """confirmation for new test
        @summary: display confirmation window with yes, no , cancel buttons 
        and returns boolean as per user event
        @note: Can only be called from the main UI thread
        @return: True if the yes button is clicked
                 False if it no button is clicked
                 nothing if cancel button is clicked
        """
        self.checkUIThread()
        dlg = wx.MessageDialog(self,\
                               "Your changes will be lost , you want to continue?", \
                               "Confirm", wx.YES|wx.NO)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            return True
        elif result == wx.ID_NO:
            return False


    def fillTopMenu (self):
        """Setting up the menu.
        @summary: This function fills the top menu and links it entries to this
        class event functions
        @note: Can only be called from the main UI thread
        @return: None
        """
        
        self.checkUIThread()
        
        #File menu
        fileMenu = wx.Menu()        
        exitMenuItemId = wx.NewId()
        exitMenuItem = fileMenu.Append (
            exitMenuItemId, \
            "E&xit", \
            " Terminate the program")
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        
        #Help menu
        helpMenu = wx.Menu()
        aboutMenuItemId = wx.NewId()
        aboutMenuItem = helpMenu.Append (aboutMenuItemId, \
                                         "&About", \
                                         "Information about this program")
        self.Bind (wx.EVT_MENU, self.onAbout, aboutMenuItem)
        helpMenu.AppendSeparator ()

        contentsMenuItemId = wx.NewId ()
        contentsMenuItem = helpMenu.Append ( \
            contentsMenuItemId, \
            "&Contents", \
            " Documentation of the program")
        self.Bind (wx.EVT_MENU, self.onContents, contentsMenuItem)

        #Menu bar
        menuBar = wx.MenuBar ()
        # Adding the "File" menu to the MenuBar
        menuBar.Append (fileMenu,"&File")
        # Adding the "Help" menu to the MenuBar
        menuBar.Append (helpMenu,"&Help")
        # Adding the MenuBar to the Frame content.
        self.SetMenuBar (menuBar)

    def getInstallPath(self):
        """getInstallPath
        @summary: Gets ATE's installation folder
        @return: string containing the backslashed Full path
                 of the installation folder
        """
        import winreg
        #Read from the registry HKLM SOFTWARE\Alstom\ATE "Install_Dir" "$INSTDIR"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Alstom\CFAT") as key:
            install_dir = winreg.QueryValueEx(key, "Install_Dir")
        return install_dir[0]

    def onContents (self, event):
        """on Contents
        @summary: loads a browser in a separate window and displays the help
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        import subprocess
        self.checkUIThread()
        #Find installation path
        #installPath = self.getInstallPath()
        #fullPath = installPath + str('/doc/CFAT_Manual.pdf')
        import os
        #os.chdir("..")
        print (os.path.abspath(os.curdir))
        docFolderPath = os.path.abspath(os.curdir)
        fullPath = docFolderPath + str('\doc\CFAT_UserManual.pdf')
        #fullPath = "../../doc/CFAT_Manual.pdf"
        if exists(fullPath):
            subprocess.Popen(fullPath,shell=True)
        else:
            self.printLog("Documentation to found:%s\n"%fullPath)


    def onAbout (self, event):
        """on about
        @summary:
        Method handling the 'about' message
        called when the help/about menu entry is clicked
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        versionFile = open("Setup\\CFATVersion.txt","r")
        version = versionFile.read()
        dlg = wx.MessageDialog (self, \
            "COMTRADE Files Analysis Tool "+version+"\n" \
            "Using Python 3.4\n" \
            "Copyright(C) 2016 Alstom Grid a GE company\n\n" \
            "Written by Alex Payet, Ajay Koliwad and Ganeshkumar Patil\n", \
            "About", style=wx.OK)
        dlg.ShowModal()
        del dlg

    def onClear (self, event):
        """on clear
        @summary: Clear the log widget
        Called when the "white page" icon button is pressed
        @note: The log widget is a list and every line is an item of that list
        @param event: wx event unused parameter
                      required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        self._logBox.SetValue("")
        self.triggerResetSuccesses()
        self.triggerResetFailures()

    def onExitNoQuestion (self, event):
        """on exit
        @summary: Method called when the user requests the application to be
        terminated.
        @param event: wx event unused parameter
              required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        if hasattr (self, "runConfigWindow"):
            selectedProject = self._SelectedProject
            self.runConfigWindow.writeSingleValue ( \
                key = "LAST_PROJECT", \
                value = selectedProject)
            if hasattr(self.runConfigWindow, "_logger"):
                self.runConfigWindow._logger.close()
            del self.runConfigWindow
        self.stopListeningLog ()
        #self._app.Exit()
        res = self.Destroy ()
        if not res:
            raise Exception ("Window not successfully destroyed")

    def onExit (self, event):
        """on exit
        @summary: Method called when the user requests the application to be
        terminated.
        @param event: wx event unused parameter
              required in all wx event handlers
        @return: None
        """
        self.checkUIThread()
        #save the current project
        self.closing = True
        dlg = wx.MessageDialog (self, \
            "Do you really want to close this application?", \
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.onExitNoQuestion(event)

    def enableRun (self, event):
        """Enables the run button
        @summary:
        Will be triggered by the scripts thread when finished to enable running
        another thread again. This is done since the scripts should not use the
        main thread since this would prevent the application from updating its
        display. ut yet we do not want two scripts to run at the same time.
        @param event: wx event unused parameter
              required in all wx event handlers
        @note: Needs to be called from the application's main thread
        @return: None
        """
        self.checkUIThread()
        self._runButton.Enable()

    def onRun (self, event):
        """ Event called when clicking the run button
        @summary:
        Runs all the scripts selected in the script list ListBox and prints
        their output into the logger TextCtrl
        @param event: wx event unused parameter
              required in all wx event handlers
        @note: Needs to be called from the application's main thread
        @return: None
        """
        self.checkUIThread()
        #Reset both progress bars
        self._testProgressBar.SetValue (0)

        self._runButton.Disable()
        self.triggerEnableStopButton(True)
                        
        """Implement functionality to read COMTRADE file path, CFAT_Configuration.xml path
        and output directory path from mainwindow
        """
        self._testLauncher = gct_select(self, INPUT_DIRECTORY=self._comtradeFolderSelectPath.GetValue(),\
                                 XML_FILE=self._configFileSelectPath.GetValue(),\
                                 TEST_OUTPUT_DIRECTORY=self._outputFolderSelectPath.GetValue())

        self.triggerEnableStopButton(True)
        #self._runButton.Enable()        
    
    def _logWidgetHandler (self):
        """Log Thread.
        @summary:
        This thread pools for available data on stdout
        When data is incoming, it informs the UI by posting an event
        so the data can be print in the UI's main thread
        @note: called from another thread than the main application one
               so please no direct calls to the HMI in here
        @return: None
        """
        out = None
        return
        while True:
            #First pull from the buffer
            if self._want_abort:
                return
            sys.stdout.flush()
            if self._want_abort:
                sys.stdout = backup
                return
            if hasattr(sys.stdout,"getvalue"):
                out = sys.stdout.getvalue()
            if self._want_abort:
                return
            if out:
                #out = sys.stdout.readline()
                wx.PostEvent (self, LogAvailableEvent(out))
            #When the program wants to terminate, this will be set.
            #Then, it will be the time to stop that thread
            if self._want_abort:
                sys.stdout = backup
                return
            sleep(0.1)

    def stopListeningLog (self):
        """stopListeningLog
        @summary:
        Tells the logger thread to stop
        @return: None
        """
        self._want_abort = True
        #unlock the logger thread by writing to stdout so its read
        #Gets something
        print ("bye!")
        #Leave enough time for the thread to stop
        sleep(2)

    def updateLogDisplayNoLog (self, event):
        """Updates the log window
        @summary:
        This one will be called in the window's main thread so it is safe to
        manipulate widgets in here
        @note: Can only be called from the main UI thread
        @return: None
        """
        self.checkUIThread()
        line = event.data
        self.printLog (line + "\n")

    def updateLogDisplay (self, event):
        """Updates the log window and logs
        @summary:
        This one will be called in the window's main thread so it is safe to
        manipulate widgets in here
        @param event: wx event unused parameter
              required in all wx event handlers
        @note: Needs to be called from the application's main thread
        @return: None
        """
        self.checkUIThread()
        line = event.data
        self.printLog(str(line) + "\n")
        if self.logger:
            self.logger.log(line + "\n")

    def startListeningLog (self):
        """Start listening log
        @summary:
        Creates a new thread to listen to log message and handle them properly
        @return: None
        """
        self._want_abort = False
        self.Connect(-1, -1, EVT_LOGAVAIL_ID, self.updateLogDisplay)
        self.Connect(-1, -1, EVT_LOGGED_ID, self.updateLogDisplayNoLog)
        thread.start_new_thread(self._logWidgetHandler,())

    def run (self):
        """run
        @summary:
        Starts the application's main loop
        @param None
        @return: None
        @note: returns when the application is closing
        """
        self.checkUIThread()
        self._app.MainLoop()

    def printLog (self, text):
        """Print log
        @summary:
        Final function called within the main window's applicative thread
        to add a message into the log widget
        @note: Can only be called from the main UI thread
        @param text: text to display, will be displayed as it, no newline
                     will be added
        @return: None
        """
        self.checkUIThread()
        self._logBox.AppendText ("%s"%text)    

#EOF
