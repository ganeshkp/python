
import pyComtrade, os, datetime, time
import xml.dom.minidom
from XML import XMLRead

INDEX_SIGNAL_NAME=9

class DigitalSignals():
    def __init__(self, cfgData, datData):
        """initializes class self variables

        @summary: This function initializes all self variables of class

        @param: None

        @return: None
        """         
        self.digital_DAT_File=list(datData)
        self.digital_Cfg_File=list(cfgData)
        self.faultInducedSample=0
 
    #-------------------------------------------------------------------------------            
    def getDigitalSignalInfo(self, signalName):
        """read data and configuration information of signal

        @summary: This function returns data and configuration information of the signal

        @param: signalName - Name of the signal

        @return: data_info - Data information of the signal
                 cfg_info - Configuration information of the signal
        """            
        for i in range(0,len(self.digital_DAT_File)):
            data_info = self.digital_DAT_File[i]
            cfg_info = self.digital_Cfg_File[i]
            
            if(signalName == cfg_info[INDEX_SIGNAL_NAME]):
                return data_info, cfg_info
            else:
                data_info, cfg_info=([] for i in range(2))
        return data_info, cfg_info 
                      
    #-------------------------------------------------------------------------------        
    def processDigitalSignals(self, xmlFilePath):
        """process all digital signals

        @summary: This function processes digital signals and prints the data into HTML. 
                  It analyzes digital signals for first transitions, all transitions.
                  It also identifies the signal which are remained 0 and 1. 

        @param: xmlFilePath - XML file name with full path

        @return: None
        """         
        remainZeroSignals=[]
        remainOneSignals=[]
        data2=[]
        xmlObj = XMLRead(xmlFilePath)        
      
        for i in range(0,len(self.digital_DAT_File)):
            data_info = self.digital_DAT_File[i]
            cfg_info = self.digital_Cfg_File[i]
            fs = cfg_info[10]*10 #Multiplied by 10, since there is bug in comtrade file
            startTime = datetime.datetime(2000+cfg_info[7][2],cfg_info[7][0],cfg_info[7][1], cfg_info[7][3], cfg_info[7][4], cfg_info[7][5], cfg_info[7][6])
            transitionFlag=0
            for j in range(0,len(data_info)-1):
                updateTime = startTime + datetime.timedelta(seconds=((j+1)*(1/fs)))
                if(data_info[j] == 0):
                    if(data_info[j+1] == 1):
                        transitionFlag=1
                        data1=[cfg_info[9],'High',updateTime,str(j+1)]
                        data2.append(data1)
                        #print(cfg_info[9],"transitioned from from 0 to 1 @",updateTime)
                if (data_info[j] == 1):
                    if(data_info[j+1] == 0):
                        transitionFlag=1
                        data1=[cfg_info[9],'Low',updateTime,str(j+1)]
                        data2.append(data1)
                        #print(cfg_info[9],'transitioned from from 1 to 0 @',updateTime)
                                 
            #Summary of signals which are 0 or 1
            if(transitionFlag == 0):
                if(data_info[0]==0):
                    signaldata = [cfg_info[9], xmlObj.getSignalDescription(cfg_info[9]), '0', 'None']
                    remainZeroSignals.append(signaldata)
                    #remainZeroCount = remainZeroCount + 1
                elif (data_info[0]==1):
                    signaldata = [cfg_info[9], xmlObj.getSignalDescription(cfg_info[9]), '1', 'None']
                    remainOneSignals.append(signaldata)
                    #remainOneCount = remainOneCount + 1

        #Create dictionary with time as Key
        dictionary={}
        timeConsideredFlag=0
        for i in range(0,len(data2)):
            timeConsideredFlag=0
            data4=[]    

            # Check time is already considered
            if data2[i][2] in dictionary.keys():
                timeConsideredFlag=1
       
            if timeConsideredFlag ==0:
                data3=data2[i][0]+','+data2[i][1]+','+data2[i][3]
                data4.append(data3)
    
                for j in range(i+1,len(data2)):
                    if(data2[i][2] == data2[j][2]):
                        data3 = data2[j][0] + ',' + data2[j][1]+','+data2[j][3]
                        data4.append(data3)
                dictionary[data2[i][2]] = data4

        #Calculate relative time and print in time ascending order
        keytemp=0
        keytemp1=0
        allTransQ,tempList,firstTransQ,firstTransSignals = ([] for i in range(4))
        for key in sorted(dictionary):
            if(keytemp1 == 0): 
                keytemp1 = key
                time=key
                tempVar1 = dictionary[key]
                for i in range(len(tempVar1)):
                    tempList = [tempVar1[i].split(',')[0], xmlObj.getSignalDescription(tempVar1[i].split(',')[0]), tempVar1[i].split(',')[1], '0', time.time()]
                    self.faultInducedSample = tempVar1[i].split(',')[2]
                    self.faultInducedSignal = tempVar1[i].split(',')[0]
                    allTransQ.append(tempList)
                    if (tempVar1[i].split(',')[0]) not in firstTransSignals:
                        firstTransSignals.append(tempVar1[i].split(',')[0])
                        firstTransQ.append(tempList)     
                #print("%s: %s: %s" % (time.time(), keytemp, dictionary[key]))
                #print("%s: %s: %s" % (time, keytemp, dictionary[key]))
            else:
                keytemp = key-keytemp1
                time=key
                                
                tempVar1 = dictionary[key]
                for i in range(len(tempVar1)):
                    tempList = [tempVar1[i].split(',')[0], xmlObj.getSignalDescription(tempVar1[i].split(',')[0]), tempVar1[i].split(',')[1], (keytemp.microseconds/1000), time.time()]
                    allTransQ.append(tempList)
                    if tempVar1[i].split(',')[0] not in firstTransSignals:
                        firstTransSignals.append(tempVar1[i].split(',')[0])
                        firstTransQ.append(tempList) 
                #print("%s: %s %s: %s" % (time.time(), (keytemp.microseconds/1000),'ms', dictionary[key]))
                #print("%s: %s %s: %s" % (time, (keytemp.microseconds/1000),'ms', dictionary[key]))                
        
        from HTML import HTMLPrint
        generateHTML=HTMLPrint()               
        generateHTML.writefirstTransQ(firstTransQ)        
        generateHTML.writeToHTMLRemainZeroSignals(remainZeroSignals)
        generateHTML.writeToHTMLRemainOneSignals(remainOneSignals)
        generateHTML.writeAllSignalTransition(allTransQ)
        
        #print(remainZeroCount,' Signals remained 0 which are:',remainZeroSignals)
        #print(remainOneCount,' Signals remained 1 which are:',remainOneSignals)
        
    #----------------------------------------------------------------------------
    def getFaultInducedSample(self):
        """returns sample at which fault is induced

        @summary: This function returns sample at which fault is induced.

        @param: None

        @return: self.faultInducedSample - sample at which fault is induced
        """          
        return self.faultInducedSample
    #-------------------------------------------------------------------------------
    def getFaultInducedSignal(self):
        """returns signal name of the fault induced

        @summary: This function returns signal name of the fault induced

        @param: None

        @return: self.faultInducedSignal - signal name of the fault induced
        """           
        return self.faultInducedSignal                                  
        
        