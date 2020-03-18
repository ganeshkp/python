
import xml.dom.minidom
class XMLRead():
    def __init__(self, xml_file):
        """initializes HTML self variables

        @summary: This function initializes all self variables when each object created.

        @param: None

        @return: None
        """
        self.xmlFile = xml_file

    #-------------------------------------------------------------------------------    
    def getReferenceDirectory(self):
        """Gets the reference folder name with full path

        @summary: This function returns Reference directory path for comparision

        @param: None

        @return: Reference directory path
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Cross_Correlation'):
                for x in analysis.getElementsByTagName('param'):
                    return(x.getAttribute('value'))     
    #-------------------------------------------------------------------------------    
    def getPercentageChangeVal(self):
        """Gets the Percentage of change value

        @summary: This function returns percentage of change value.

        @param: None

        @return: percentage of change value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Smoothed_Increase'):
                for x in analysis.getElementsByTagName('param'):
                    return(x.getAttribute('value')) 
                
    #-------------------------------------------------------------------------------
    def getSignalDescription(self, signalID):
        """Gets the signal description for the signal

        @summary: This function receives signal name and returns signal description.

        @param: signalID - Signal ID

        @return: Description of the signal
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        signalList = collection.getElementsByTagName("signal")
        for signal in signalList:
            if(signalID == signal.getAttribute('id')):
                return signal.getAttribute('description')
            
    #-------------------------------------------------------------------------------    
    def getMaxPeaksToDetect(self):
        """Gets maximum number of peaks to detect

        @summary: This function returns maximum number of peaks to detect.

        @param: None

        @return: maximum number of peaks to detect
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Peak_Detection'):
                for x in analysis.getElementsByTagName('param'):
                    return(x.getAttribute('value')) 
    #-------------------------------------------------------------------------------    
    def getMaxHarmonicsToDetect(self):
        """Gets the maximum number of harmonics to detect

        @summary: This function returns maximum number of harmonics to detect

        @param: None

        @return: maximum number of harmonics to detect
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Discontinity'):
                for x in analysis.getElementsByTagName('param'):
                    return(x.getAttribute('value')) 
    #-------------------------------------------------------------------------------    
    def getPU(self):
        """Gets the power unit value

        @summary: This function returns power unit value.

        @param: None

        @return: Power Unit value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Commutation'):
                for x in analysis.getElementsByTagName('param'):
                    if(x.getAttribute('name') == "PU"):
                        return(x.getAttribute('value')) 
    #-------------------------------------------------------------------------------    
    def getCurrentDivFACPHC(self):
        """Gets the currentDivFACPHC value

        @summary: This function returns currentDivFACPHC value.

        @param: None

        @return: currentDivFACPHC value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Commutation'):
                for x in analysis.getElementsByTagName('param'):
                    if(x.getAttribute('name') == "currentDivFACPHC"):
                        return(x.getAttribute('value')) 
    #-------------------------------------------------------------------------------    
    def getCommFailSetThrePHC(self):
        """Gets the commFailSetThrePHC value

        @summary: This function returns commFailSetThrePHC value.

        @param: None

        @return: commFailSetThrePHC value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Commutation'):
                for x in analysis.getElementsByTagName('param'):
                    if(x.getAttribute('name') == "commFailSetThrePHC"):
                        return(x.getAttribute('value'))
    #-------------------------------------------------------------------------------    
    def getCommFailResetThrePHC(self):
        """Gets the commFailResetThrePHC value

        @summary: This function returns commFailResetThrePHC value.

        @param: None

        @return: commFailResetThrePHC value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Commutation'):
                for x in analysis.getElementsByTagName('param'):
                    if(x.getAttribute('name') == "commFailResetThrePHC"):
                        return(x.getAttribute('value'))
    #-------------------------------------------------------------------------------    
    def getCommFailTC(self):
        """Gets the commFailTC value

        @summary: This function returns commFailTC value.

        @param: None

        @return: commFailTC value
        """          
        DomTree = xml.dom.minidom.parse(self.xmlFile)
        collection = DomTree.documentElement
        for analysis in collection.getElementsByTagName("Analysis"):
            if(analysis.getAttribute('id') == 'Commutation'):
                for x in analysis.getElementsByTagName('param'):
                    if(x.getAttribute('name') == "commFailTC"):
                        return(x.getAttribute('value'))