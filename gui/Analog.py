
import os, datetime, operator,pyComtrade
from scipy.signal import butter, filtfilt
#from peakutils.plot import plot as pplot
from matplotlib import pyplot
from time import mktime
from HTML import HTMLPrint
import xml.dom.minidom
from Digital import DigitalSignals
from XML import XMLRead
import numpy as np
from numpy.fft import fft, ifft, fftshift
from ReadComtrade import ReadComtrade

CORR_SHIFT_OFFSET = 50
SAMPLE_COUNT_250MS=4465
SAMPLE_COUNT_150MS=2679
INDEX_START_TIME=15
INDEX_SIGNAL_NAME=17
INDEX_SAMPLING_RATE=18
INDEX_UU=7
INDEX_TIME=19
TOTAL_SIGNALS_COMM_FAIL=8

class AnalogSignals():
    
    def __init__(self, mainWindow, cfgData, datData):
        """initializes all the self variables to 0

        @summary: This function initializes all the self variables to 0.

        @param: None

        @return: None
        """ 
        self.Number_of_Comtrade_Files=0
        self.analog_DAT_File=list(datData)
        self.analog_Cfg_File=list(cfgData)
        self.writeToHTML=""
        self.xmlFile=""   
        self.mainWindow = mainWindow  
   
        
    def readComtradeFiles(self, folderpath):
        """Reads signal information which is stored in COMTRADE data format

        @summary: This function gets folder path and reads all data and configuration
                  information of the analog signal.

        @param: folderpath - Folder path where all comtrade files are stored.

        @return: None
        """         
        self.mainWindow.triggerLogAvailable("Reading COMTRADE files\n")
        #Get all the configuration files
        CfgFileList = []
        for name in os.listdir(folderpath):
            if name.endswith(".cfg"):
                if(os.path.getsize(folderpath+'\\'+name) > 0):
                    CfgFileList.append(name)

        #Define List arrays
        listb=[]
        self.Number_of_Comtrade_Files=len(CfgFileList)
        
        for k in range(len(CfgFileList)):
            file_name = os.path.join(folderpath,CfgFileList[k])
            self.filename = file_name
            print(file_name)
            self.mainWindow.triggerLogAvailable("Reading: " + file_name)
            
            comtradeObj1 = pyComtrade.ComtradeRecord(file_name)
            t = comtradeObj1.getTime()
        
            for i in range(comtradeObj1.A):
                self.analog_DAT_File.append(comtradeObj1.getAnalogChannelData(i+1))
                self.analog_key.append(comtradeObj1.Ach_id[i])
                listb = ['A', \
                         comtradeObj1.station_name, \
                         comtradeObj1.rec_dev_id, \
                         comtradeObj1.rev_year,\
                         comtradeObj1.An[i], \
                         comtradeObj1.Aph[i], \
                         comtradeObj1.Accbm[i], \
                         comtradeObj1.uu[i],\
                         comtradeObj1.a[i], \
                         comtradeObj1.b[i], \
                         comtradeObj1.skew[i], \
                         comtradeObj1.min[i],\
                         comtradeObj1.max[i], \
                         comtradeObj1.primary, \
                         comtradeObj1.secondary, \
                         comtradeObj1.start,\
                         comtradeObj1.trigger, \
                         comtradeObj1.Ach_id[i], \
                         comtradeObj1.getSamplingRate(), \
                         t]
                self.analog_Cfg_File.append(listb)       
#---------------------------------------------------------------------------------------

    def processAnalogSignals(self, dirName, faultSample, xmlFile):
        """function to process all analog signals

        @summary: This function processes all analog signals and also reads type of fault analysis
                  to be performed on the analog signal and processes based on it.

        @param: faultSample - sample number at which fault is induced
                refAnalogDATFile - data information of the reference signal
                refAnalogCfg - configuration information of the reference signal
                referenceFaultSample - sample at which fault is induced on reference data
                xmlFile - XML file name

        @return: None
        """         
        self.mainWindow.triggerLogAvailable("Analog Signal Processing started\n")
        self.xmlFile = xmlFile
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement        
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Cross_Correlation'):
                try:
                    xmlObj = XMLRead(self.xmlFile)
                    refPath = xmlObj.getReferenceDirectory()
                    refFolder =  refPath + "\\" + dirName
                    self.mainWindow.triggerLogAvailable("Reading Reference directory: "+refFolder)
                    readComtrade = ReadComtrade(refFolder)
                    digCfgFile,digDataFile = readComtrade.getDigitalComtradeInfo()
                    refDigitalData = DigitalSignals(digCfgFile, digDataFile)
                    refDigitalData.processDigitalSignals(self.xmlFile)
                    referenceFaultSample = refDigitalData.getFaultInducedSample()
                    self.mainWindow.triggerLogAvailable("Reference signal first fault induced at sample: "+referenceFaultSample)
                    analogCfgFile, analogDataFile = readComtrade.getAnalogComtradeInfo()
                    referenceAnalogData = AnalogSignals(self.mainWindow, analogCfgFile, analogDataFile)
                    break
                except Exception as err:
                    print("Reference directory and COMTRADE folder under analysis should have same named subfolders\n")
                    self.mainWindow.enableRunButton()
                    exit(0)                    
     
        inputData=[]
        self.writeToHTML = HTMLPrint()
        self.writeToHTML.peakSignalsHTML(1, inputData)
        self.writeToHTML.smoothTransSignalsHTML(1, inputData)
        self.writeToHTML.nonContinuousSignalsHTML(1, inputData) 
        self.writeToHTML.corrSignalsHTML(1, inputData)
        self.writeToHTML.summaryCorrSignalsHTML(1, inputData)
        self.writeToHTML.commFailHTML(1, inputData)

        #Perform Analysis of analof signals
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Peak_Detection'):
                self.mainWindow.triggerLogAvailable("Performing PEAK Detection\n")
                for x in analysis.getElementsByTagName('signal'):
                    signalName = x.getAttribute('id')
                    data_info, cfg_info=([] for i in range(2))
                    data_info, cfg_info = self.getAnalogSignalInfo(signalName)
                    if len(data_info) !=0:
                        fs = cfg_info[INDEX_SAMPLING_RATE]*10 #Multiplied by 10, since there is bug in comtrade file
                        self.mainWindow.triggerLogAvailable("Detecting peaks for signal: "+signalName)
                        self.processPeakSignals(data_info, cfg_info, fs, faultSample)   
            if(analysis.getAttribute('id') == 'Smoothed_Increase'):
                for x in analysis.getElementsByTagName('signal'):
                    signalName = x.getAttribute('id')
                    data_info, cfg_info=([] for i in range(2))
                    data_info, cfg_info = self.getAnalogSignalInfo(signalName)
                    if len(data_info) !=0:
                        fs = cfg_info[INDEX_SAMPLING_RATE]*10 #Multiplied by 10, since there is bug in comtrade file
                        self.mainWindow.triggerLogAvailable("Detecting Smooth Transition for signal: "+signalName)
                        self.processSmoothTransitionSignals(data_info, cfg_info, fs, faultSample)
            if(analysis.getAttribute('id') == 'Discontinity'):
                for x in analysis.getElementsByTagName('signal'):
                    signalName = x.getAttribute('id')
                    data_info, cfg_info=([] for i in range(2))
                    data_info, cfg_info = self.getAnalogSignalInfo(signalName)
                    if len(data_info) !=0:
                        fs = cfg_info[INDEX_SAMPLING_RATE]*10 #Multiplied by 10, since there is bug in comtrade file
                        self.mainWindow.triggerLogAvailable("Detecting Discontinuity for signal: "+signalName)
                        self.processNonContinuousSignals(data_info, cfg_info, fs)
            if(analysis.getAttribute('id') == 'Cross_Correlation'):
                for x in analysis.getElementsByTagName('signal'):
                    signalName = x.getAttribute('id')
                    data_info, cfg_info=([] for i in range(2))
                    data_info, cfg_info = self.getAnalogSignalInfo(signalName)
                    if len(data_info) !=0:
                        fs = cfg_info[INDEX_SAMPLING_RATE]*10 #Multiplied by 10, since there is bug in comtrade file
                        for j in range(0, len(referenceAnalogData.analog_DAT_File)):
                            if(cfg_info[INDEX_SIGNAL_NAME] == referenceAnalogData.analog_Cfg_File[j][INDEX_SIGNAL_NAME]):
                                ref_data_info = referenceAnalogData.analog_DAT_File[j]
                                ref_cfg_info=referenceAnalogData.analog_Cfg_File[j]
                                self.mainWindow.triggerLogAvailable("Detecting Cross correlation for signal: "+signalName)
                                self.performCrossCorrelation(data_info, cfg_info, fs, referenceFaultSample, ref_data_info, ref_cfg_info)
            if(analysis.getAttribute('id') == 'Commutation'):
                for z in analysis.getElementsByTagName('signalList'):
                    side = z.getAttribute('id')
                    setNum = z.getAttribute('set')
                    data_info1, cfg_info1 = ([] for i in range(2))
                    signalCount = 0
                    for x in z.getElementsByTagName('signal'):
                        signalName = x.getAttribute('id')
                        data_info, cfg_info=([] for i in range(2))
                        data_info, cfg_info = self.getAnalogSignalInfo(signalName)
                        #Check signal data is available
                        if len(data_info) !=0:
                            if signalName == cfg_info[INDEX_SIGNAL_NAME]:
                                data_info = data_info[:,0]
                                data_info1.append(data_info)
                                cfg_info1.append(cfg_info)
                                fs = cfg_info[INDEX_SAMPLING_RATE]#*10 
                                signalCount = signalCount+1

                    if signalCount == TOTAL_SIGNALS_COMM_FAIL:
                        self.mainWindow.triggerLogAvailable("Detecting Commutation Failure for side: "+side+ "and Set number: "+setNum)                           
                        self.detectCommFail(data_info1, cfg_info1, fs, side, setNum) 
                    else:
                        inputData=["Signal is missing for the set:", setNum]
                        self.writeToHTML.commFailHTML(4, inputData)
                                        
        inputData=[]
        self.writeToHTML.peakSignalsHTML(5, inputData) 
        self.writeToHTML.smoothTransSignalsHTML(5, inputData)
        self.writeToHTML.nonContinuousSignalsHTML(5, inputData)
        self.writeToHTML.corrSignalsHTML(4, inputData) 
        self.writeToHTML.summaryCorrSignalsHTML(3, inputData)    
        self.writeToHTML.commFailHTML(5, inputData)              
    #END OF FUNCTION           
#------------------------------------------------------------------------------------------------------------------------------

    def detectCommFail(self, data_info1, cfg_info1, fs, side, setNum):
        """Computes the shifting of reference signal from original position
        # TO BE UPDATED
        @summary: This function receives two data lists, sampling frequency, 
        side and data will be passed to low pass filter, output from filter 
        to be processed in detectCommFail for commfail detection      

        @param: data_info1      - Analog data from comtrade file
                cfg_info1       - configuration  data from comtrade file
                fs              - sampling frequency from comtrade file
                side            - XML schema for commFail
                setNum          - Set number
                #signalName      - identified signal to be processed for commFail from XML schema for debugging
        @return: # None
        """        
        #Initialize lists
        IdiffUpperBridge,IdiffLowerBridge = ([] for i in range(2))
        updateRate = 1/fs
        divergenceFactor = 0
        
        #Get constant from XML configuration file
        xmlObj = XMLRead(self.xmlFile)
        PU = float(xmlObj.getPU())
        currentDivFACPHC = float(xmlObj.getCurrentDivFACPHC())
        commFailSetThrePHC = float(xmlObj.getCommFailSetThrePHC())
        commFailResetThrePHC = float(xmlObj.getCommFailResetThrePHC())
        commFailTC = float(xmlObj.getCommFailTC())
        pA = updateRate/(updateRate+commFailTC)
        pB = commFailTC/(updateRate+commFailTC)
        
        title = 'UpperBridgePre' 
        pIvwUpperBridgePre,pIvwUpperBridge = ([] for i in range(2))
        a = [x+y for x,y in zip( abs(data_info1[0]), abs(data_info1[1]))]
        pIvwUpperBridgePre = [x+y for x,y in zip( a, abs(data_info1[2]))]
        pIvwUpperBridgePreNew = [i * pA for i in pIvwUpperBridgePre]
        for i in range(0, len(pIvwUpperBridgePreNew)):
            if not i:
                pIvwUpperBridge.append(pIvwUpperBridgePreNew[i])
            else:
                pIvwUpperBridge.append(pIvwUpperBridgePreNew[i]+pB*pIvwUpperBridge[i-1]) 
        
        title = 'LowerBridge'
        pIvwLowerBridge,pIvwLowerBridgePre=([] for i in range(2))
        a = [x+y for x,y in zip( abs(data_info1[3]), abs(data_info1[4]))]
        pIvwLowerBridgePre = [x+y for x,y in zip( a, abs(data_info1[5]))]
        pIvwLowerBridgePreNew = [i * pA for i in pIvwLowerBridgePre]
        for i in range(0, len(pIvwLowerBridgePreNew)):
            if not i:
                pIvwLowerBridge.append(pIvwLowerBridgePreNew[i])
            else:
                pIvwLowerBridge.append(pIvwLowerBridgePreNew[i]+pB*pIvwLowerBridge[i-1]) 
        
        pIdc,pIdcPre = ([] for i in range(2))
        pIdcPre = data_info1[7]
        pIdcPreNew = [i * pA for i in pIdcPre]
        for i in range(0, len(pIdcPreNew)):
            if not i:
                pIdc.append(pIdcPreNew[i])
            else:
                pIdc.append(pIdcPreNew[i]+pB*pIdc[i-1])        
     
        pCurrentOrder = data_info1[6]
        divergenceFactor       = currentDivFACPHC * (pCurrentOrder*PU)
        commFailSetThreshold   = divergenceFactor + (commFailSetThrePHC*PU)
        commFailResetThreshold = divergenceFactor + (commFailResetThrePHC*PU)
        # DC > AC detection
        IdiffUpperBridge = [x-y for x,y in zip( pIdc, pIvwUpperBridge)] 
        IdiffLowerBridge = [x-y for x,y in zip( pIdc, pIvwLowerBridge)]        
        A1 = np.greater_equal(IdiffUpperBridge, commFailSetThreshold)
        A2 = np.greater_equal(IdiffLowerBridge, commFailSetThreshold)

        title = 'UpperBridgeCommFail' 
        time =list(range(0,len(IdiffUpperBridge))) 
        s1 = []
        IdiffUpperBridgecomfail=[]
        for i in range(0, len(IdiffUpperBridge)):
            if (A1[i] == 1):
                s1.append(i)
                IdiffUpperBridgecomfail.append(IdiffUpperBridge[i])
        
        if len(s1) !=0:
            startSampleUpperBridge = s1[0]
            lastSample = len(s1)
            endSampleUpperBridge = s1[lastSample-1]
            temp = datetime.timedelta(seconds=((startSampleUpperBridge)*(1/fs)))
            temp1=temp.seconds*2000
            temp2=temp.microseconds/1000
            startTimeUB = temp1+temp2
            temp = datetime.timedelta(seconds=((endSampleUpperBridge)*(1/fs)))
            temp1=temp.seconds*2000
            temp2=temp.microseconds/1000
            endTimeUB = temp1+temp2
            inputData = ['Upper Bridge', startSampleUpperBridge, endSampleUpperBridge, startTimeUB, endTimeUB, commFailSetThreshold[startSampleUpperBridge], commFailSetThreshold[endSampleUpperBridge], setNum]
            self.writeToHTML.commFailHTML(2, inputData)
            self.graphPlot( time, commFailSetThreshold, time, IdiffUpperBridge, s1, IdiffUpperBridgecomfail, 0,0, title , side)  
        else:
            inputData=["No commutation failure on Upper Bridge for set:", setNum]
            self.writeToHTML.commFailHTML(4, inputData)

        title = 'LowerBridgeCommFail' 
        time =list(range(0,len(IdiffLowerBridge))) 
        s2 = []
        IdiffLowerBridgecomfail=[]
        for i in range(0, len(IdiffLowerBridge)):
            if (A2[i] == 1):
                s2.append(i)
                IdiffLowerBridgecomfail.append(IdiffLowerBridge[i])

        if len(s2) !=0:
            startSampleLowerBridge = s2[0]
            lastSample = len(s2)
            endSampleLowerBridge = s2[lastSample-1]
            temp = datetime.timedelta(seconds=((startSampleLowerBridge)*(1/fs)))
            temp1=temp.seconds*2000
            temp2=temp.microseconds/1000
            startTimeLB = temp1+temp2
            temp = datetime.timedelta(seconds=((endSampleLowerBridge)*(1/fs)))
            temp1=temp.seconds*2000
            temp2=temp.microseconds/1000
            endTimeLB = temp1+temp2
            inputData = ['Lower Bridge', startSampleLowerBridge, endSampleLowerBridge, startTimeLB, endTimeLB, commFailSetThreshold[startSampleLowerBridge], commFailSetThreshold[endSampleLowerBridge], setNum]
            self.writeToHTML.commFailHTML(2, inputData)
            self.graphPlot( time, commFailSetThreshold, time, IdiffLowerBridge, s2, IdiffLowerBridgecomfail, 0,0, title , side)
        else:
            inputData=["No commutation failure on Lower Bridge for set:", setNum]
            self.writeToHTML.commFailHTML(4, inputData)
        
    #------------------------------------------------------------------------------------------------------------------------------
    def graphPlot(self, time1, data1, time2, data2, time3, data3, time4, data4, title, side):
        """Computes the shifting of reference signal from original position
        # TO BE UPDATED
        @summary: This method can receive 4 data lists (X-dimensional and Y-dimensional ) 
        and polt the same accordingly. 

        @param: x - 1-dimensional array of the signal(time1, time2, time2 and time 4)
                y - 1-dimensional array of the signal(data1, data2, data3 and data 4)
                title and side to be used for save the plots

        @return: None
        # TO BE UPDATED
        """
        pyplot.figure(figsize=(8,5))
        pyplot.plot(time1, data1,'b', time2, data2, 'g', time3, data3, 'r', time4, data4, 'k')
        pyplot.title(title)
        pyplot.xlabel('time')
        pyplot.ylabel('Amp')
        name1 = './GRAPHS/small/' + title + side + '.png'
        pyplot.savefig(name1)
        figure=pyplot.gcf()
        name2 = './GRAPHS/large/' + title + side + '.png'
        figure.set_size_inches(8, 5)
        pyplot.savefig(name2, dpi=600)

        inputData=[name1, name2]
        self.writeToHTML.commFailHTML(3, inputData)        
        pyplot.close('all')        
    #-------------------------------------------------------------------------------------------------    
    # shift &lt; 0 means that y starts 'shift' time steps before x # shift &gt; 0 means that y starts 'shift' time steps after x
    def _compute_shift(self, x, y):
        """Computes the shifting of reference signal from original position

        @summary: This function receives two signals and computes number of shifts to be done 
                  other signal to make it maximum correlated.

        @param: x - 1-dimensional array of the signal
                y - 1-dimensional array of the signal 

        @return: shift - returns the shift value
        """ 
        assert len(x) == len(y)
        f1 = fft(x)
        f2 = fft(np.flipud(y))
        cc = np.real(ifft(f1 * f2))
        c = fftshift(cc)
        assert len(c) == len(x)
        zero_index = int(len(x) / 2) - 1
        shift = zero_index - np.argmax(c)
        return shift
    #-------------------------------------------------------------------------------
    def _butter_lowpass_filtfilt(self, data, cutoff, fs, order=5):
        """Performs smoothening of the signal

        @summary: This function receives signal data information and smoothes the signal.

        @param: data - data information of the signal
                cutoff - cutoff value
                fs - Sampling frequency
                order = 5 - This is fixed value.
        @return: None
        """            
        nyq = 0.5 * fs
        normal_cutoff=0
        if(nyq!=0):
            normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data, axis=-1, padtype='even', padlen=None, method='pad', irlen=None)
        return y
    #End of function
        
    #-------------------------------------------------------------------------------    
    def _match(self, x, ref, faultInjectedSample):
        """Finds the match between the 2 signals

        @summary: This function finds match behaviour of the 2 signals

        @param: x - One dimensionals array of the signal
                ref - One dimensional array of reference signal
                faultInjectedSample - Sample at which fault injected

        @return: None
        """ 
        shiftPosition=0
        M = len(x) + len(ref) - 1
        N = 2 ** int(np.ceil(np.log2(M)))
        X = np.fft.rfft(x, N)
        Y = np.fft.rfft(ref, N)
        cxy = np.fft.irfft(X * np.conj(Y))
        cxy = np.hstack((cxy[:len(x)], cxy[N-len(ref)+1:]))    
        index = np.argmax(cxy)
        if index < len(x):
            shiftPosition= index
        else: # negative lag
            shiftPosition= index - len(cxy) 
        
        if(shiftPosition <= CORR_SHIFT_OFFSET):
            shiftPosition = faultInjectedSample  
        return shiftPosition 
    #-------------------------------------------------------------------------------
    def performCrossCorrelation(self, data_info, cfg_info, fs, faultInjectedSample, ref_data_info, ref_cfg_info):
        """Finds the correlation between the two signals

        @summary: This function find the correlation between the 2 signals

        @param: data_info - DAT file information of signal under analysis
                cfg_info - cfg file information of the signal under analysis
                fs - Sampling frequency
                faultInjectedSample - Sample at which fault is injected
                ref_data_info - DAT file information of reference signal
                ref_cfg_info - cfg file information of reference signal                

        @return: None
        """ 
        data_info = data_info[:,0]
        ref_data_info=ref_data_info[:,0]
        faultInjectedSample=int(faultInjectedSample)

        #4465 is considered to make it as 250ms
        temp_ref1=[]
        for i in range(faultInjectedSample,faultInjectedSample+SAMPLE_COUNT_250MS):
            temp_ref1.append(ref_data_info[i])

        # Perform Correlation
        shift = self._match(data_info[0:faultInjectedSample+SAMPLE_COUNT_250MS], temp_ref1, faultInjectedSample)
        coeff = np.corrcoef(data_info[faultInjectedSample:faultInjectedSample+SAMPLE_COUNT_250MS], temp_ref1)[0,1]
        coherence_percent = float("{0:.2f}".format((coeff*coeff) * 100))      

        temp_ref2=[]
        for i in range(0,shift):
            temp_ref2.append(0)
        temp_ref2=temp_ref2+temp_ref1[0:shift+SAMPLE_COUNT_250MS-faultInjectedSample]  
        
        #Convert to time samples into milliseconds
        time2=list(range(1,len(temp_ref2)+1))
        for i in range(0,len(time2)):
            temp = datetime.timedelta(seconds=((i)*(1/fs)))
            time2[i] = temp.microseconds/1000   
            
        faultTemp = datetime.timedelta(seconds=((faultInjectedSample)*(1/fs)))
        faultInjectedinMs = faultTemp.microseconds/1000 
        
        shiftTemp = datetime.timedelta(seconds=((shift)*(1/fs)))
        shiftInMs = shiftTemp.microseconds/1000
        
        xmlObj = XMLRead(self.xmlFile)
        inputData = [cfg_info[INDEX_SIGNAL_NAME], xmlObj.getSignalDescription(cfg_info[INDEX_SIGNAL_NAME]), str(shiftInMs), str(faultInjectedinMs), str(coherence_percent)]
        self.writeToHTML.corrSignalsHTML(2, inputData)
        
        diff = shift - faultInjectedSample
        absdiff=0
        if diff < 0:
            absdiff = abs(diff)
        diffTemp = datetime.timedelta(seconds=((absdiff)*(1/fs)))
        diffInMs = diffTemp.microseconds/1000
        
        if diff < 0:
            diffInMs = -diffInMs
        
        inputData = [cfg_info[INDEX_SIGNAL_NAME], str(diffInMs), str(coherence_percent)]
        self.writeToHTML.summaryCorrSignalsHTML(2, inputData)        
        
        # Plot the graph
        pyplot.figure(figsize=(8,5))
        pyplot.plot(time2, data_info[0:len(temp_ref2)])
        pyplot.xlabel('time (mS)')
        pyplot.ylabel(cfg_info[INDEX_UU])
        pyplot.axvline(faultInjectedinMs, color='r', linestyle='--')
        pyplot.plot(time2, temp_ref2)
        pyplot.title(cfg_info[INDEX_SIGNAL_NAME])
        name1 = './GRAPHS/small/' + cfg_info[INDEX_SIGNAL_NAME] + '_correlation' + '.png'
        pyplot.savefig(name1)
        figure=pyplot.gcf()
        name2 = './GRAPHS/large/' + cfg_info[INDEX_SIGNAL_NAME] + '_correlation' + '.png'
        figure.set_size_inches(8, 5)
        pyplot.savefig(name2, dpi=600)
        inputData=[name1, name2]
        self.writeToHTML.corrSignalsHTML(3, inputData)
        pyplot.close('all')      
       
    #-------------------------------------------------------------------------------
    def processSmoothTransitionSignals(self, data_info, cfg_info, fs, faultInjectedSample):
        """Process the Smooth transitioning of the signal

        @summary: Receives data and configuration information of the signal and 
        finds the time where signal changes (increase/decrease) in terms of specified 
        percentage in XML and prints the report.

        @param: data_info - data information of the signal
                cfg_info - Configuration information of the signal
                fs - Sampling frequency
                faultInjectedSample - sample at which fault is induced

        @return: None
        """           
        faultInjectedSample = int(faultInjectedSample)

        data_info = data_info[:,0]
        power_smooth = self._butter_lowpass_filtfilt(data_info, 100, fs)
                
        startTime = datetime.datetime(2000+cfg_info[15][2],cfg_info[15][0],cfg_info[15][1], cfg_info[15][3], cfg_info[15][4], cfg_info[15][5], cfg_info[15][6])
        transitionFlag=0
        
        xmlObj = XMLRead(self.xmlFile)
        inputData = [cfg_info[INDEX_SIGNAL_NAME], xmlObj.getSignalDescription(cfg_info[INDEX_SIGNAL_NAME])]
        self.writeToHTML.smoothTransSignalsHTML(2, inputData)
    
        #Get the value of signal when fault is induced
        x = power_smooth[faultInjectedSample]
        xtime = startTime + datetime.timedelta(seconds=((faultInjectedSample)*(1/fs)))
        xtimeInMs = (mktime(xtime.timetuple()) + xtime.microsecond/1000000.0)*1000
        xmlObj = XMLRead(self.xmlFile)
        percent_change = xmlObj.getPercentageChangeVal()
        
        for j in range(faultInjectedSample, len(power_smooth)-1):
            if transitionFlag > 3:
                break
            updateTime = startTime + datetime.timedelta(seconds=((j)*(1/fs)))   
            updateTimeInMs =  (mktime(updateTime.timetuple()) + updateTime.microsecond/1000000.0)*1000    
            #if(abs(x-power_smooth[j]) >= float(percent_change)*transitionFlag):
            #if((abs(x)-abs(power_smooth[j])) >= abs(x*float(percent_change)*transitionFlag)):
            if(abs(x-power_smooth[j]) >= abs(x*float(percent_change)*transitionFlag)):
                inputData = [str(updateTimeInMs-xtimeInMs), str(power_smooth[j]), str(int(float(percent_change)*transitionFlag*100)), str(updateTime.time())]     
                self.writeToHTML.smoothTransSignalsHTML(3, inputData)           
                transitionFlag = transitionFlag + 1


        time=cfg_info[INDEX_TIME]
        
        #Convert to time samples into milliseconds
        for i in range(0,len(time)):
            temp = datetime.timedelta(seconds=((i)*(1/fs)))
            time[i] = temp.microseconds/1000
            
        faultTemp = datetime.timedelta(seconds=((faultInjectedSample)*(1/fs)))
        faultInjectedinMs = faultTemp.microseconds/1000
        
        #Plot the graph
        pyplot.figure(figsize=(8,5))
        pyplot.plot(time, data_info)
        pyplot.plot(time, power_smooth)
        pyplot.title(cfg_info[INDEX_SIGNAL_NAME])
        pyplot.xlabel('time (mS)')
        pyplot.ylabel(cfg_info[INDEX_UU])
        pyplot.axvline(faultInjectedinMs, color='r', linestyle='--')
        name1 = './GRAPHS/small/' + cfg_info[INDEX_SIGNAL_NAME] + '_smoooth'+ '.png'
        pyplot.savefig(name1)
        figure=pyplot.gcf()
        name2 = './GRAPHS/large/' + cfg_info[INDEX_SIGNAL_NAME] + '_smoooth'+ '.png'
        figure.set_size_inches(8, 5)
        pyplot.savefig(name2, dpi=600)
        inputData=[name1, name2]
        self.writeToHTML.smoothTransSignalsHTML(4, inputData)
        pyplot.close('all')     
        
    #End of processSmoothTransitionSignals
    #-------------------------------------------------------------------------------    
    def processPeakSignals(self, data_info, cfg_info, fs, faultInjectedSample):
        """Process the peaks of the signal

        @summary: Receives data and configuration information of the signal and 
        finds the highest positive and negative peaks of the signal. It also calculates
        Pre fault and Post fault mean and standard deviation of the signal

        @param : data_info - data information of the signal
                     cfg_info - Configuration information of the signal
                     fs - Sampling frequency
                     faultInjectedSample - sample at which fault is induced

        @return: None
        """        
        xmlObj = XMLRead(self.xmlFile)
        faultInjectedSample=int(faultInjectedSample)
        
        y = data_info[:,0]
        time = cfg_info[INDEX_TIME]
        startTime = datetime.datetime(2000+cfg_info[INDEX_START_TIME][2],\
                                           cfg_info[INDEX_START_TIME][0],\
                                           cfg_info[INDEX_START_TIME][1],\
                                           cfg_info[INDEX_START_TIME][3],\
                                           cfg_info[INDEX_START_TIME][4],\
                                           cfg_info[INDEX_START_TIME][5],\
                                           cfg_info[INDEX_START_TIME][6])
        xtime = startTime + datetime.timedelta(seconds=(faultInjectedSample*(1/fs)))
        #Convert to time samples into milliseconds
        for i in range(0,len(time)):
            temp = datetime.timedelta(seconds=((i)*(1/fs)))
            time[i] = temp.microseconds/1000
        
        preFaultMean = np.mean(data_info[0:faultInjectedSample])
        preFaultStd = np.std(data_info[0:faultInjectedSample])
        
        #peakdetect method to identify both positive and negative peaks
        max_peaks, min_peaks= self._peakdetect(y[0:faultInjectedSample+SAMPLE_COUNT_150MS], lookahead=1)
        posPeakDict = {}
        negPeakDict={}
       
        for i in range(0,len(max_peaks)):
            posPeakDict[max_peaks[i][0]] = max_peaks[i][1]
            
        for i in range(0,len(min_peaks)):
            negPeakDict[min_peaks[i][0]] = min_peaks[i][1]
            
        posPeakD = sorted(posPeakDict.items(), key=operator.itemgetter(1), reverse=True)[:int(xmlObj.getMaxPeaksToDetect())]
        negPeakD = sorted(negPeakDict.items(), key=operator.itemgetter(1), reverse=False)[:int(xmlObj.getMaxPeaksToDetect())]
    
        sortedDict = posPeakD+negPeakD
        
        peakIndexes=[]
        for i in range(len(sortedDict)):
            peakIndexes.append(sortedDict[i][0])
       
        inputData=[]
        if(len(sortedDict) > 0):
            #Get the maximum sample at which peaks are considered            
            maxTime = max(sortedDict)[0]  
            postFaultMean = np.mean(data_info[maxTime:len(y)])
            postFaultStd = np.std(data_info[maxTime:len(y)])   

            inputData = [cfg_info[INDEX_SIGNAL_NAME], xmlObj.getSignalDescription(cfg_info[INDEX_SIGNAL_NAME]), str(preFaultMean), str(preFaultStd), str(postFaultMean), str(postFaultStd)]
            self.writeToHTML.peakSignalsHTML(2, inputData)

            for i in range(0,len(sortedDict)):
                inputData=[]
                sample = sortedDict[i][0]
                updateTime = startTime+datetime.timedelta(seconds=((sample)*(1/fs)))
                t1 = updateTime - xtime
                inputData=[str(t1.microseconds/1000), str(y[sample]), str(updateTime.time())]
                self.writeToHTML.peakSignalsHTML(3, inputData)
      
            #print(updateTime.time(),':',cfg_info[INDEX_SIGNAL_NAME],'Peak value:',y[sample])  
            faultTemp = datetime.timedelta(seconds=(faultInjectedSample*(1/fs)))
            faultInjectedinMs = faultTemp.microseconds/1000
            
            # pyplot.figure(figsize=(8,5))
            # pplot(time[0:faultInjectedSample+SAMPLE_COUNT_150MS], y[0:faultInjectedSample+SAMPLE_COUNT_150MS], peakIndexes)
            # pyplot.title(cfg_info[INDEX_SIGNAL_NAME])
            # pyplot.xlabel('time (mS)')
            # pyplot.ylabel(cfg_info[INDEX_UU])
            # pyplot.axvline(faultInjectedinMs, color='r', linestyle='--')
            # name1 = './GRAPHS/small/' + cfg_info[INDEX_SIGNAL_NAME] + '_peak'+ '.png'
            # pyplot.savefig(name1)
            # figure=pyplot.gcf()
            # name2 = './GRAPHS/large/' + cfg_info[INDEX_SIGNAL_NAME] + '_peak'+ '.png'
            # figure.set_size_inches(8, 5)
            # pyplot.savefig(name2, dpi=600)
            # inputData=[name1, name2]
            # self.writeToHTML.peakSignalsHTML(4, inputData)
            # pyplot.close('all')
    
    #End of processPeakSignals
    #-------------------------------------------------------------------------------
    def processNonContinuousSignals(self, data_info, cfg_info, fs):
        """Process the non-continuous signal

        @summary: received data and configuration information of the signal and process 
        the non-continuous signal and finds list of maximum Amplitudes and corresponding frequencies.

        @param : data_info - data information of the signal
                     cfg_info - Configuration information of the signal
                     fs - Sampling frequency

        @return: None
        """  
        xmlObj = XMLRead(self.xmlFile)
        y = data_info[:,0]
        time=cfg_info[INDEX_TIME]
        listx=[0,0]
        #Convert to time samples into milliseconds
        for i in range(0,len(time)):
            temp = datetime.timedelta(seconds=((i)*(1/fs)))
            time[i] = temp.microseconds/1000
     
        startTime = datetime.datetime(2000+cfg_info[15][2],cfg_info[15][0],cfg_info[15][1], cfg_info[15][3], cfg_info[15][4], cfg_info[15][5], cfg_info[15][6])
        startSampleTime=0
        EndSampleTime=0
        startFlag = 0
        counter = 0
       
        #Get Continuous Signal Start and End time
        for i in range(0, len(y)-1):        
            if(y[i] != 0):
                if startFlag == 0:
                    startSampleTime=i
                    startFlag=1
            if(y[i]-y[i+1] == 0):
                counter=counter+1
                if(EndSampleTime == 0):
                    EndSampleTime = i
            else:
                counter = 0
                EndSampleTime = 0
        if(counter >= 100):
            listx = [startSampleTime,EndSampleTime]
        else:
            listx = [startSampleTime, len(y)]
        #End for loop
        
        startTimeSample = listx[0]
        endTimeSample = listx[1]
        length = endTimeSample-startTimeSample
            
        fft_y = fft(y[startTimeSample:endTimeSample])
        freqs = np.fft.fftfreq(length)
        fs=fs/10
        freq_in_hertz = abs(freqs*fs)[:int(len(freqs)/2)]
        Ampl = np.abs(fft_y)[0:int(len(freqs)/2)]
        frqTable = dict(zip(Ampl,freq_in_hertz))           
   
        signalPartStartTime = startTime+datetime.timedelta(seconds=((startTimeSample)*(1/fs)))
        signalPartEndTime = startTime+datetime.timedelta(seconds=((endTimeSample)*(1/fs)))
        #print('       ','From Start Time:',signalPartStartTime.time(),'to End Time:',signalPartEndTime.time(),'has top 5 frequencies:',selected_freq,'top 5 magnitudes:',selected_Ampl)
        
        inputData=[cfg_info[INDEX_SIGNAL_NAME], xmlObj.getSignalDescription(cfg_info[INDEX_SIGNAL_NAME]), str(signalPartStartTime.time()), str(signalPartEndTime.time())]
        self.writeToHTML.nonContinuousSignalsHTML(2, inputData)
        
        selectedAmpl = sorted(Ampl, reverse=True)[:int(xmlObj.getMaxHarmonicsToDetect())]
        for i in range(0, len(selectedAmpl)):
            inputData=[str(i+1), str(frqTable[selectedAmpl[i]]), str(selectedAmpl[i])]
            self.writeToHTML.nonContinuousSignalsHTML(3, inputData)
    
        #Plot graph
        N=length
        pyplot.figure(figsize=(8,5))
        xf = freq_in_hertz[0:int(N/2)]
        pyplot.plot(xf, fft_y[0:int(N/2)])
        pyplot.title(cfg_info[INDEX_SIGNAL_NAME])
        pyplot.xlabel('Frequency (Hz)')
        pyplot.ylabel(cfg_info[INDEX_UU])
        name1 = './GRAPHS/small/' + cfg_info[INDEX_SIGNAL_NAME] + '_FFT'+'.png'
        pyplot.savefig(name1)
        figure=pyplot.gcf()
        name2 = './GRAPHS/large/' + cfg_info[INDEX_SIGNAL_NAME] + '_FFT'+'.png'
        figure.set_size_inches(8, 5)
        pyplot.savefig(name2, dpi=600)
        inputData=[name1, name2]
        self.writeToHTML.nonContinuousSignalsHTML(4, inputData)
        pyplot.close('all')        
        
#------------------------------------------------------------------------------------
    def getAnalogSignalInfo(self, signalName):
        """provides analog signal information

        @summary: Receives signal name and provide data and configuration information of the signal.

        @param : signalName - name of the signal

        @return: data_info - Data information of the signal
                 cfg_info - Configuration information of the signal
        """  
        data_info=[]
        cfg_info = []
        for i in range(0,len(self.analog_DAT_File)):
            data_info = self.analog_DAT_File[i]
            cfg_info = self.analog_Cfg_File[i]
            
            if(signalName == cfg_info[INDEX_SIGNAL_NAME]):
                return data_info, cfg_info
            else:
                data_info=[]
                cfg_info=[]
        
        return data_info, cfg_info

#------------------------------------------------------------------------------------
    def _datacheck_peakdetect(self, x_axis, y_axis):
        """perform the data check the input array

        @summary: This function returns an array of x-axis and y axis to make
        sure that length of both arrays are same

        @param : x_axis -- A x-axis whose values correspond to the y_axis list
                 y_axis -- A list containing the signal over which to find peaks

        @return: x_axis - x-axis 1- dimensional array
                 y_axis - y-axis 1- dimensional array
        """  
        if x_axis is None:
            x_axis = range(len(y_axis))
        
        if len(y_axis) != len(x_axis):
            raise ValueError( 
                    "Input vectors y_axis and x_axis must have same length")
        
        #needs to be a numpy array
        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)
        return x_axis, y_axis
#------------------------------------------------------------------------------------
    def _peakdetect(self, y_axis, x_axis = None, lookahead = 200, delta=0):
        """Detects maximas and minima of the signal

        @summary: Converted from/based on a MATLAB script at: 
           http://billauer.co.il/peakdet.html
        
        function for detecting local maxima and minima in a signal.
        Discovers peaks by searching for values which are surrounded by lower
        or larger values for maxima and minima respectively
        

        @param : 
                y_axis -- A list containing the signal over which to find peaks
                
                x_axis -- A x-axis whose values correspond to the y_axis list and is used
                    in the return to specify the position of the peaks. If omitted an
                    index of the y_axis is used.
                    (default: None)
                
                lookahead -- distance to look ahead from a peak candidate to determine if
                    it is the actual peak
                    (default: 200) 
                    '(samples / period) / f' where '4 >= f >= 1.25' might be a good value
                
                delta -- this specifies a minimum difference between a peak and
                    the following points, before a peak may be considered a peak. Useful
                    to hinder the function from picking up false peaks towards to end of
                    the signal. To work well delta should be set to delta >= RMSnoise * 5.
                    (default: 0)
                        When omitted delta function causes a 20% decrease in speed.
                        When used Correctly it can double the speed of the function
            
        @return: two lists [max_peaks, min_peaks] containing the positive and
                negative peaks respectively. Each cell of the lists contains a tuple
                of: (position, peak_value) 
                to get the average peak value do: np.mean(max_peaks, 0)[1] on the
                results to unpack one of the lists into x, y coordinates do: 
                x, y = zip(*max_peaks)
        """
        max_peaks = []
        min_peaks = []
        dump = []   #Used to pop the first hit which almost always is false
           
        # check input data
        x_axis, y_axis = self._datacheck_peakdetect(x_axis, y_axis)
        # store data length for later use
        length = len(y_axis)
        
        
        #perform some checks
        if lookahead < 1:
            raise ValueError("Lookahead must be '1' or above in value")
        if not (np.isscalar(delta) and delta >= 0):
            raise ValueError("delta must be a positive number")
        
        #maxima and minima candidates are temporarily stored in
        #mx and mn respectively
        mn, mx = np.Inf, -np.Inf
        
        #Only detect peak if there is 'lookahead' amount of points after it
        for index, (x, y) in enumerate(zip(x_axis[:-lookahead], 
                                           y_axis[:-lookahead])):
            if y > mx:
                mx = y
                mxpos = x
            if y < mn:
                mn = y
                mnpos = x
            
            ####look for max####
            if y < mx-delta and mx != np.Inf:
                #Maxima peak candidate found
                #look ahead in signal to ensure that this is a peak and not jitter
                if y_axis[index:index+lookahead].max() < mx:
                    max_peaks.append([mxpos, mx])
                    dump.append(True)
                    #set algorithm to only find minima now
                    mx = -np.Inf
                    mn = np.Inf
                    if index+lookahead >= length:
                        #end is within lookahead no more peaks can be found
                        break
                    continue
            
            ####look for min####
            if y > mn+delta and mn != -np.Inf:
                #Minima peak candidate found 
                #look ahead in signal to ensure that this is a peak and not jitter
                if y_axis[index:index+lookahead].min() > mn:
                    min_peaks.append([mnpos, mn])
                    dump.append(False)
                    #set algorithm to only find maxima now
                    mn = np.Inf
                    mx = -np.Inf
                    if index+lookahead >= length:
                        #end is within lookahead no more peaks can be found
                        break
       
        #Remove the false hit on the first value of the y_axis
        try:
            if dump[0]:
                max_peaks.pop(0)
            else:
                min_peaks.pop(0)
            del dump
        except IndexError:
            #no peaks were found, should the function return empty lists?
            pass
            
        return [max_peaks, min_peaks]
    