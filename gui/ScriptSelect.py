
import sys
import ctypes
import os

try:
    #Python 2.7
    import thread
except ImportError:
    #python 3.xx
    import _thread as thread

from os.path import isdir

from mainwindow import CFATMainWindow



class ScriptSelect:
    """ This class handles command line arguments and creates the main window
    """
    def __init__(self):
        """Initialises the ScriptSelection's class
        """
        # Create a new app, don't redirect stdout/stderr to a window.

        # Top-level window.
        self._aselogPath = None
        self._projectName = None
        self._svnUserName = None
        self._svnPassword = None
        self._ateFile = None

    def printHelp(self):
        """Displays the help
        @summary:
        Text contents are taken from the above file comment, to update on
        line help, simply edit the above commentary
        @return: None
        """
        print (__doc__)

    def parseArgs (self, args):
        """Parse the script's arguments

        @summary: Whenever this function is modified, please ensure the script's
        documentation is updated so that printHelp always prints an up-to-date
        documentation of this script.

        @param args: scripts arguments to be handled by this function

        @return: None In some cases, this function will not even return as
                 it will call exit()
        """
        #Non command line version by default
        self.nonInteractive = False
        if "-h" in args or "--help" in args:
            self.printHelp()
            exit(0)
        if "-r" in args or "--run" in args:
            self._run = True
        else:
            self._run = False
        if "-X" in args or "--quit" in args:
            self._quit = True
        else:
            self._quit = False
        if "-p" in args or "--project" in args:
            try:
                index = args.index ("-p")
                if index is None or index < 0:
                    index = args.index("--project")
                #Get the next element
                self._projectName = args [index + 1]
            except Exception as err:
                print ("invalid -p or --project command line argument (%s)\n"%err)
                self.printHelp()
                exit(2)

        if "-f" in args or "--file" in args:
            #ATE command line option, will load the next file, run it and exit
            try:
                #Get the index of the option
                index = args.index ("-f")
                if index is None or index < 0:
                    index = args.index("--file")
                #Get the next element
                self._ateFile = args [index + 1]
                #Check it is a valid folder else display error message,
                #printHelp and quit
                if not os.path.isfile (self._ateFile):
                    raise Exception("Not a valid ate filename:%s"%self._ateFile)
                else:
                    # Check if project is valid
                    loadFile = ateFile (self._ateFile)
                    ateProjectFile = loadFile.getProject()
                    self._scriptList = loadFile.getScripts()
                    ps = ProjectSpecificsModel.getInstance()
                    if ps.projectExists(ateProjectFile):
                        if None in self._scriptList:
                            print ("Project Name (%s) is getting loaded and No script is added for execution under the project"%ateProjectFile)
                            #self.printLog ("Project Name (%s) is getting loaded and No script is added for execution under the project"%ateProjectFile)
                        else:   
                            print ("Project Name (%s) is getting loaded and executed\n"%ateProjectFile)
                    else:
                        print ("Invalid Project Name %s Mentioned inside "\
                        "ate file %s\n"%(ateProjectFile,self._ateFile))
                        exit(2)
                        
                #Command line version
                self.nonInteractive = True
            except Exception as err:
                print ("invalid -f or --file command line argument or invalid XML structure(%s)\n"%err)
                self.printHelp()
                exit(1)
        
        #set dummysession true or false
        if "-d" in args or "--dummyon" in args:
            self.dummy = True
        elif "-n" in args or "--dummyoff" in args:
            self.dummy=False
        else:
            self.dummy = None
        #set log folder path through command line options
        if "-l" in args or "--logFolder" in args:
            #ATE command line option, will load the next logFolder path, to save the log files
            try:
                #Get the index of the option
                index = args.index ("-l")
                if index is None or index < 0:
                    index = args.index("--logFolder")
                #Get the next element
                self._aselogPath = args [index + 1]
                #Check it is a valid folder path else display error message,
                #printHelp and quit
                if not os.path.isdir (self._aselogPath) or not os.path.exists(self._aselogPath):
                    raise Exception("Not a valid ate log folder path:%s"%self._aselogPath)
                #Command line version
                self.nonInteractive = True
            except Exception as err:
                print ("invalid -l or --logFolder command line argument (%s)\n"%err)
                self.printHelp()
                exit(1)

        if "-rtLd" in args or "--RTDSLoadModel" in args:
            self.loadRTDS = 'True'
        elif "-rtNoLd" in args or "--RTDSNoLoadModel" in args:
            self.loadRTDS = 'False'
        else:
            self.loadRTDS = None
            
        #set SVN Username 
        if "-sUName" in args or "--SvnUserName" in args:
            #ATE command line option, specifying SVN Username
            try:
                #Get the index of the option
                index = args.index ("-sUName")
                if index is None or index < 0:
                    index = args.index("--SvnUserName")
                #Get the next element
                self._svnUserName = str(args [index + 1])
            except Exception as err:
                print ("invalid -sUName or --SvnUserName command line argument (%s)\n"%err)
                self.printHelp()
                exit(1)

        #set SVN Password
        if "-sPwd" in args or "--SvnPassword" in args:
            #ATE command line option, specifying SVN Username
            try:
                #Get the index of the option
                index = args.index ("-sPwd")
                if index is None or index < 0:
                    index = args.index("--SvnPassword")
                #Get the next element
                self._svnPassword = str(args [index + 1])
            except Exception as err:
                print ("invalid -sPwd or --SvnPassword command line argument (%s)\n"%err)
                self.printHelp()
                exit(1)

        #Open an empty sqlite file
        if "-g" in args or "--generateNewSqlite" in args:
            self.initiateDatabase = True
            self.nonInteractive = True
        else:
            self.initiateDatabase = False
                
    def commandLineThread (self, ATEFilepath, rootFrame):
        """commandLineThread
        @summary: Thread used to simulate user input when running the
                  command line version
        @return: None
        """
        import time
        #Leave enough time for the UI to initiate
        time.sleep(5)
        if ATEFilepath:
            rootFrame.triggerLoadATEFileEvent (ATEFilepath)
        if self._run:
            rootFrame.triggerRunEvent ()
        if self.initiateDatabase:
            self.bmWindow = rootFrame.getBMWindow ()
            
            self.bmWindow.initiateDatabase (checkRequiredKeys=True)
            if self._quit:
                rootFrame.triggerASEClose()
        if self._quit:
            rootFrame.shouldQuitWhenDone ()

    def run (self, rootFrame):
        """
        TODO
        """
        if self.nonInteractive:
            thread.start_new_thread ( \
                self.commandLineThread, \
                (self._ateFile,rootFrame))

if __name__ == '__main__':
    try:
        #This needs to be kept for windows 7
        #or the application's icon will be based on python.exe
        myappid = 'ge.pes.ate.1.2.15'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        #On windows XP it fails since the function's not there
        #But that's fine since the icon is there on XP
        #So just ignore the error silently
        pass
    scriptSelectInstance=ScriptSelect()
    scriptSelectInstance.parseArgs(sys.argv)
    rootFrame = CFATMainWindow (None, \
                title = "Comtrade File Analysis Tool", \
                logFolder = scriptSelectInstance._aselogPath
                )
    scriptSelectInstance.run (rootFrame)
    rootFrame.run ()
    del rootFrame
    os._exit(0)