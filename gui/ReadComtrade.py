
import pyComtrade, os
from mainwindowNonUI import CFATMainWindowNonUI

class ReadComtrade():
    """ This class handles reading comtrade files for analog and digital signals
    """    
    def __init__(self, folderpath):
        """initializes all the self variables

        @summary: This function initializes all the self variables with comtrade data
                  for analog and digital signals

        @param: None

        @return: None
        """ 
        self.mainWindowNonUI = CFATMainWindowNonUI.getInstance()
        self.analog_DAT_File=[]
        self.analog_Cfg_File=[]
        self.digital_DAT_File=[]
        self.digital_Cfg_File=[]
        
        #Get all the configuration files
        CfgFileList = []
        for name in os.listdir(folderpath):
            if name.endswith(".cfg"):
                if(os.path.getsize(folderpath+'\\'+name) > 0):
                    CfgFileList.append(name)

        #Read data based in configuration files
        for k in range(len(CfgFileList)):
            listb=[]
            file_name = os.path.join(folderpath,CfgFileList[k])
            self.filename = file_name
            print(file_name)
            self.mainWindowNonUI.triggerLogAvailable(file_name)
            
            comtradeObj1 = pyComtrade.ComtradeRecord(file_name)
            t = comtradeObj1.getTime()
            
            #Read digital signal data
            for i in range(comtradeObj1.D):
                if(comtradeObj1.ft == "ASCII\n"):
                    self.digital_DAT_File.append(comtradeObj1.getDigitalChannelData(i+1))
                elif(comtradeObj1.ft == "BINARY\n"):
                    self.digital_DAT_File.append(comtradeObj1.getDigitalChannelBinaryData(i+1))
                else:
                    pass

                listb = ['D', \
                         comtradeObj1.station_name, \
                         comtradeObj1.rec_dev_id, \
                         comtradeObj1.Dn[i], \
                         comtradeObj1.Dph[i], \
                         comtradeObj1.Dccbm, \
                         comtradeObj1.y, \
                         comtradeObj1.start, \
                         comtradeObj1.trigger, \
                         comtradeObj1.Dch_id[i], \
                         comtradeObj1.getSamplingRate(), \
                         t]
                self.digital_Cfg_File.append(listb) 
        
            #Read Analaog signal data
            for i in range(comtradeObj1.A):
                listb=[]
                if(comtradeObj1.ft == "ASCII\n"):
                    self.analog_DAT_File.append(comtradeObj1.getAnalogChannelData(i+1))
                elif(comtradeObj1.ft == "BINARY\n"):
                    self.analog_DAT_File.append(comtradeObj1.getAnalogChannelBinaryData(i+1))
                else:
                    pass
                
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
                
          
    def getAnalogComtradeInfo(self):
        """returns analog comtrade data

        @summary: This function returns comtrade data for analog signals

        @param: None

        @return: None
        """  
        return self.analog_Cfg_File, self.analog_DAT_File
    
    def getDigitalComtradeInfo(self):
        """returns digital comtrade data

        @summary: This function returns comtrade data for digital signals
        
        @param: None

        @return: None
        """  
        return self.digital_Cfg_File, self.digital_DAT_File
        
    