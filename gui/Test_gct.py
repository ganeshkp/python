

try:
    #Python 2.7
    import thread
except ImportError:
    #python 3.xx
    import _thread as thread
    from importlib import reload
import glob, os, shutil, sys
from Analog import AnalogSignals
from Digital import DigitalSignals
from HTML import HTMLPrint
from ReadComtrade import ReadComtrade
from mainwindowNonUI import CFATMainWindowNonUI

class gct_select:
    """ This class handles command line arguments and creates the main window
    """
    def __init__(self, mainWindow, INPUT_DIRECTORY, XML_FILE, TEST_OUTPUT_DIRECTORY, start=True):
        """Initialises the gct_select's class"""
        self._inputDirectory = INPUT_DIRECTORY
        self._xmlFile = XML_FILE
        self._outputDir = TEST_OUTPUT_DIRECTORY
        self.mainWindow = mainWindow
        self.mainWindowNonUI = CFATMainWindowNonUI.getInstance()
        if start:
            thread.start_new_thread(self._run,(INPUT_DIRECTORY,XML_FILE,TEST_OUTPUT_DIRECTORY))
    
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
        if "-h" in args or "--help" in args:
            self.printHelp()
            exit(0)

        if "-f" in args or "-folderPath" in args:
            # Command line option, will load the folder path, run it and exit
            try:
                #Get the index of the option
                if "-f" in args:
                    index = args.index("-f")
                elif "-folderPath" in args:
                    index = args.index("-folderPath")
                #Get the next element
                self._faultsFolder = args[index + 1]
                #Check if it is a valid folder path else display error
                #Print Help and quit
                if not os.path.isdir(self._faultsFolder) or not os.path.exists(self._faultsFolder):
                    raise Exception("Not a valid folder name : %s"%self._faultsFolder)
            except Exception as err:
                print ("invalid -f or -folderPath command line argument (%s)\n"%err)
                self.printHelp()
                exit(1)
                
        if "-x" in args or "-xmlFileName" in args:
            # xml file command line option, will run the next file, run it and exit
            try:
                #Get the index of the option
                if "-x" in args:
                    index = args.index("-x")
                elif "-xmlFileName" in args:
                    index = args.index("-xmlFileName")
                #Get the next element
                self._xmlFile = args[index + 1]
                #Check if it is a valid file name else display error
                #Print Help and quit
                if not os.path.isfile(self._xmlFile):
                    raise Exception("Not a valid file name : %s"%self._xmlFile)
            except Exception as err:
                print ("invalid -x or -xmlFileName command line argument (%s)\n"%err)
                self.printHelp()
                exit(2)

        if "-t" in args or "-testOutputFolder" in args:
            # Command line option, will load the output folder path, run it and exit
            try:
                #Get the index of the option
                if "-t" in args:
                    index = args.index("-t")
                elif "-testOutputFolder" in args:
                    index = args.index("-testOutputFolder")
                #Get the next element
                self._outputFolder = args[index + 1]
                #Check if it is a valid folder path else display error
                #Print Help and quit
                if not os.path.isdir(self._outputFolder) or not os.path.exists(self._outputFolder):
                    raise Exception("Not a valid file name : %s"%self._outputFolder)
            except Exception as err:
                print ("invalid -t or -testOutputFolder command line argument (%s)\n"%err)
                self.printHelp()
                exit(3)
				
        if len(sys.argv) >= 1:
            #Check the length of the passed argument
            #print ("=========================================sys.argv======================", len(sys.argv))
            try:
                INPUT_DIRECTORY = scriptSelectInstance._faultsFolder 
                XML_FILE = scriptSelectInstance._xmlFile
                TEST_OUTPUT_DIRECTORY = scriptSelectInstance._outputFolder
                return (INPUT_DIRECTORY,XML_FILE,TEST_OUTPUT_DIRECTORY)
            except Exception as error:
                #Raised the exception if argument are not available
                print("Invalid number of arguements:- Use 'Test_gct.py -h' for number of arguements to be provided ")
                exit(4)
                
    def _run (self, INPUT_DIRECTORY, XML_FILE, TEST_OUTPUT_DIRECTORY):
        """run the software

        @summary: Whenever this function is modified, please ensure the script's
        documentation is updated so that printHelp always prints an up-to-date
        documentation of this script.

        @param args: scripts arguments to be handled by this function

        @return: None In some cases, this function will not even return as
                 it will call exit()
        """
        #path = bytes(SERVER_DIRECTORY, "utf-8").decode("unicode_escape")
        print(INPUT_DIRECTORY)
        self.mainWindow.triggerLogAvailable("Selected Folder: " + INPUT_DIRECTORY)
        dirList = ([d for d in os.listdir(INPUT_DIRECTORY) if os.path.isdir(os.path.join(INPUT_DIRECTORY, d))])
        print(dirList)
        #self.mainWindow.triggerLogAvailable("Directory List: " + dirList)
        
        #Remove TEST_OUTPUT_DIRECTORY contents if any
        if(os.listdir(TEST_OUTPUT_DIRECTORY) != []):
            for root, dirs, files in os.walk(TEST_OUTPUT_DIRECTORY):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        
        HTMLInfo = HTMLPrint()
        HTMLInfo.createProto1()
        HTMLInfo.createDirListFile(dirList)
        HTMLInfo.createIndexFile()
        HTMLInfo.createHeadingFile()
        
        for x in dirList:           
            temp = INPUT_DIRECTORY+ "\\" + x
            print (x)
            self.mainWindow.triggerLogAvailable("Selected Sub Directory: " + x)
            comtradeInfo = ReadComtrade(temp)
            digitalCfgFile,digitalDataFile = comtradeInfo.getDigitalComtradeInfo()
            
            #Process Digital data
            digitalData = DigitalSignals(digitalCfgFile, digitalDataFile)
            digitalData.processDigitalSignals(XML_FILE)            
            if(os.path.exists(TEST_OUTPUT_DIRECTORY+'/'+x) == 0):
                os.mkdir(TEST_OUTPUT_DIRECTORY+'/'+x)
            shutil.copy('dig1.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/dig1.html')
            shutil.copy('dig2.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/dig2.html')
            shutil.copy('dig3.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/dig3.html')
            shutil.copy('dig4.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/dig4.html') 
                
            faultSample = digitalData.getFaultInducedSample()
            self.mainWindow.triggerLogAvailable("First fault induced at sample: " +faultSample)

            #Process Analog data
            if(os.path.exists('GRAPHS') == 0):
                os.mkdir('GRAPHS')
            if(os.path.exists('GRAPHS/small') == 0):
                os.mkdir('GRAPHS/small')
            if(os.path.exists('GRAPHS/large') == 0):
                os.mkdir('GRAPHS/large')
    
            analogCfgFile,digitalDataFile = comtradeInfo.getAnalogComtradeInfo()            
            analogData = AnalogSignals(self.mainWindow, analogCfgFile, digitalDataFile)
            analogData.processAnalogSignals(x, faultSample, XML_FILE)
                    
            shutil.copy('Proto1.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Proto1.html')
            shutil.copy('Analog1.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Analog1.html')
            shutil.copy('Analog2.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Analog2.html')
            shutil.copy('Analog3.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Analog3.html')
            shutil.copy('Analog4.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Analog4.html')
            shutil.copy('Analog5.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/Analog5.html')
            shutil.copy('heading.html',TEST_OUTPUT_DIRECTORY+'/'+x+'/heading.html')     
            shutil.copytree('GRAPHS',TEST_OUTPUT_DIRECTORY+'/'+x+'/GRAPHS')
            #Delete all graphs
            shutil.rmtree('GRAPHS')
    
        shutil.copy('Index.html',TEST_OUTPUT_DIRECTORY+'/Index.html')
        shutil.copy('directoryList.html',TEST_OUTPUT_DIRECTORY+'/directoryList.html')
        shutil.copytree('MetroUI',TEST_OUTPUT_DIRECTORY+'/'+'/MetroUI')
        shutil.copy('folder_open.png',TEST_OUTPUT_DIRECTORY+'/folder_open.png')
        
        #Remove all intermediate files
        for f in os.listdir(os.getcwd()):
            if f.endswith('.html'):
                os.unlink(f)
        self.mainWindow.enableRunButton()

if __name__ == '__main__':    
    scriptSelectInstance=gct_select()
    scriptSelectInstance.parseArgs(sys.argv)
    scriptSelectInstance._run(INPUT_DIRECTORY = scriptSelectInstance._faultsFolder, \
                             XML_FILE = scriptSelectInstance._xmlFile, \
                             TEST_OUTPUT_DIRECTORY = scriptSelectInstance._outputFolder)
    os._exit(0)
