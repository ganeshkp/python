
class HTMLPrint():
    def __init__(self):
        """initializes HTML self variables

        @summary: This function initializes all self variables when each object created.

        @param: None

        @return: None
        """         
        self.peakSignalFile=0
        self.nonContinuousSignalFile=0
        self.smoothSignalFile=0
        self.corSignalFile=0
        self.summaryCorrFile=0
        self.commFailFile=0

     #-------------------------------------------------------------------------------
    def createHeadingFile(self):
        """Creates heading.html HTML

        @summary: This function creates heading.html file

        @param: None

        @return: None
        """         
        f = open('heading.html','w')
        headerFooter = """<!DOCTYPE html>
<html>

<body>
    <address id="directory">Directory<br></address>
<script>
        var decoded_url = decodeURIComponent(location.pathname.split('/')[1]);
        directory.innerText = decoded_url;
        </script>
    <style>
    address {
    font-family: Georgia, "Times New Roman",
        Times, serif;
    font-size:large;
    color: red;
    margin-top: 1em;
    padding-top: 1em;
    border-bottom: thin dotted }
    </style>    
</body>

</html>\n\n"""
        f.write(headerFooter)
        f.close()
     #-------------------------------------------------------------------------------
    def createProto1(self):
        """Creates prototype HTML

        @summary: This function creates Proto1.html file which displays all digital and analog
                  fault analysis information

        @param: None

        @return: None
        """         
        f = open('Proto1.html','w')
        headerFooter = """<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="Metro, a sleek, intuitive, and powerful framework for faster and easier web development for Windows Metro Style.">
    <meta name="keywords" content="HTML, CSS, JS, JavaScript, framework, metro, front-end, frontend, web development">
    <meta name="author" content="Sergey Pimenov and Metro UI CSS contributors">

    <link rel='shortcut icon' type='image/x-icon' href='../favicon.ico' />

    <title>HVDC PES - RTDS Comtrade File Analysis </title>

    <link href="../MetroUI/css/metro.css" rel="stylesheet">
    <link href="../MetroUI/css/metro-icons.css" rel="stylesheet">
    <link href="../MetroUI/css/metro-responsive.css" rel="stylesheet">

    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src="../MetroUI/js/metro.js"></script>
    <script src="../MetroUI/js/ga.js"></script>
    <script src="../MetroUI/js/jquery.dataTables.min.js"></script>


</head>

<body>
    <script src="../MetroUI/js/w3data.js"></script>
    <div class="container  page-content">
        <div class="grid">
            <div class="row">
                <div class="cell">
                    <div class="accordion medium-heading" data-role="accordion" data-close-any="true">
                        <div class="frame">
                            <div class="heading">First Transition</div>
                            <div class="content">
                                <div class="example" data-text="First Transition">
                                    <div id="Dig1"></div>

                                </div>
                            </div>
                        </div>

                        <div class="frame">
                            <div class="heading">Stayed Low</div>
                            <div class="content">
                                <div class="example" data-text="Stayed Low">

                                    <div id="Dig2"></div>

                                </div>
                            </div>
                        </div>
                        <div class="frame">
                            <div class="heading">Stayed High</div>
                            <div class="content">
                                <div class="example" data-text="Stayed High" >
                                   <div id="Dig3"></div>
                                </div>
                            </div>
                        </div>

                        <div class="frame">
                            <div class="heading">All Transitions</div>
                            <div class="content">
                                <div class="example" data-text="All Transitions">
                                    <div id="Dig4"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="frame">
                            <div class="heading">Peaks</div>
                            <div class="content">
                                <div class="example" data-text="Peaks">
                                   <div id="Analog1"></div>
                                </div>
                            </div>
                        </div>

                        <div class="frame">
                            <div class="heading">Rise Time</div>
                            <div class="content">
                                <div class="example" data-text="Rise Time">
                                   <div id="Analog2"></div>
                                </div>
                            </div>
                        </div>

                        <div class="frame">
                            <div class="heading">FFT</div>
                            <div class="content">
                                <div class="example" data-text="FFT">
                                   <div id="Analog3"></div>
                                </div>
                            </div>
                        </div>                        
                        
                        <div class="frame">
                            <div class="heading">Correlation</div>
                            <div class="content">
                                <div class="example" data-text="Correlation">
                                   <div id="Analog4"></div>
                                </div>
                            </div>
                        </div>                  
                        <div class="frame">
                            <div class="heading">Commutation</div>
                            <div class="content">
                                <div class="example" data-text="Commutation">
                                   <div id="Analog5"></div>
                                </div>
                            </div>
                        </div>                          
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        $("#Dig1").load("Dig1.html");
        $("#Dig2").load("Dig2.html");
        $("#Dig3").load("Dig3.html");
        $("#Dig4").load("Dig4.html");
        $("#Analog1").load("Analog1.html");
        $("#Analog2").load("Analog2.html");
        $("#Analog3").load("Analog3.html");
        $("#Analog4").load("Analog4.html");
        $("#Analog5").load("Analog5.html");
        $("#SummaryCorrelation").load("SummaryCorrelation.html");
        $("#zoom_01").elevateZoom();
    </script>
</body>

</html>

\n\n"""
              
        f.write(headerFooter)
        f.close()
        
    #-------------------------------------------------------------------------------
    def createDirListFile(self, dirList):
        """Creates index.HTML file

        @summary: this function creates Index.html file which has all the directory information
                  of main folder. All the directory which points to Proto1.html of corresponding folders.

        @param: dirList - directory list

        @return: None
        """          
        f1 = open('directoryList.html','w')
        f1header = """<html>
<head>
<script language="JavaScript" type="text/javascript">
function change2frames(url)
{
var headlocation = url+'/heading.html'
var resultlocation = url+'/Proto1.html'
parent.heading.location=headlocation;
parent.results.location=resultlocation;
}
</script>
</head>
<h2>Directories</h2>
<ul class="navbar">\n\n"""
        
        f1.write(f1header)   
        for x in dirList:
            #temp = '                <td><a href="'+os.getcwd()+'\\'+testSubFolder+'\\'+x+'\Proto1.html">'+x+'</a></td>\n'
            temp = '    <li><a href="javascript:change2frames('+"'"+x+"'"+')">'+x+'<img src="folder_open.png" style="float: left" /></a>\n'
            f1.write(temp)
            
        f1base = """<style>
               ul.navbar {
                 list-style-type: none;
                 padding: 0;
                 margin: 0;
                 position: absolute;
                 top: 2em;
                 left: 1em;}
               ul.navbar li {
                 background: white;
                 margin: 0.5em 0;
                 padding: 0.3em;}
               ul.navbar a {
                 text-decoration: none
                 display: inline-block;}
               a:link {
                 color: blue }
               a:visited {
                 color: purple }
</style>
</html>\n\n"""
        f1.write(f1base)
        f1.close()      
        
    #-------------------------------------------------------------------------------
    def createIndexFile(self):
        """Creates frame HTML file

        @summary: this function creates frame.html file which displays main frame information

        @param: None

        @return: None
        """          
        f2=open('Index.html','w')
        f2header = """<html>

<FRAMESET cols="17%,*%" >
               <FRAME src="directoryList.html" name="directorieslist" frameborder="0">
               <FRAMESET rows="20%, *" frameborder="0" framespacing="0">
               <FRAME src="http://localhost:1337/1a on P3GR@1.0pu/heading.html" name="heading" >
               <FRAME src="http://localhost:1337/1a on P3GR@1.0pu/Proto1.html" name="results" scrolling=Yes >
               </FRAMESET>
</FRAMESET>
</html>\n"""
        f2.write(f2header)
        f2.close()      
    #-------------------------------------------------------------------------------
    def writefirstTransQ(self, firstTransQ):
        """Writes first transition of each signal

        @summary: This function writes first transition of each signal into dig1.html file 
                  in HTML format

        @param: firstTransQ - List containing first transition information of all digital signals

        @return: None
        """ 
        f = open('dig1.html','w')
        headerFooter = """<html>
    
        <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Signal</th>
                    <th>Description</th>
                    <th>Transition</th>
                    <th>Absolute Time</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Signal</th>
                    <th>Description</th>
                    <th>Transition</th>
                    <th>Absolute Time</th>
                </tr>
            </tfoot>
            <tbody>\n\n"""
        f.write(headerFooter)
        for i in range(0, len(firstTransQ)):
            f.write('            <tr>\n')
            temp = '                <td>'+str(firstTransQ[i][3])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(firstTransQ[i][0])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(firstTransQ[i][1])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(firstTransQ[i][2])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(firstTransQ[i][4])+'</td>\n'
            f.write(temp)
            f.write('            </tr>\n')
            
        base = """\n        </tbody>
        </table>
        <p></p>
    
    
    </html>"""
        f.write(base)
        f.close()
    #-------------------------------------------------------------------------------
    def writeToHTMLRemainZeroSignals(self, remainZeroSignals):
        """Writes signal information which are remained 0

        @summary: This function writes all the signal information which are remained 0

        @param: remainZeroSignals - List containing all remain 0 signal information

        @return: None
        """         
        f = open('dig2.html','w')
        headerFooter = """<html>
    <table id="Stayed High" class="dataTable striped border bordered" data-role="datatable" data-searching="false">
        \n    <thead>
            <tr>
                <th>Signal</th>
                <th>Description</th>
                <th>Initial State</th>
                <th>Transition</th>
            </tr>
        </thead>
    
        <tfoot>
            <tr>
                <th>Signal</th>
                <th>Description</th>
                <th>Initial State</th>
                <th>Transition</th>
            </tr>
        </tfoot>
        <tbody>\n\n"""
        f.write(headerFooter)
        for i in range(0, len(remainZeroSignals)):
            f.write('        <tr>\n')
            temp = '            <td>'+str(remainZeroSignals[i][0])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainZeroSignals[i][1])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainZeroSignals[i][2])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainZeroSignals[i][3])+'</td>\n'
            f.write(temp)
            f.write('        </tr>\n')
            
        base = """\n\n\n    </tbody>
    </table>\n
    </hhtml>"""
        f.write(base)
        f.close()
    #-------------------------------------------------------------------------------   
        
    def writeToHTMLRemainOneSignals(self, remainOneSignals):
        """Writes signal information which are remained 1

        @summary: This function writes all the signal information which are remained 1

        @param: remainOneSignals - List containing all remain 1 signal information

        @return: None
        """         
        f = open('dig3.html','w')
        headerFooter = """<html>
    <table id="Stayed High" class="dataTable striped border bordered" data-role="datatable" data-searching="false">
        \n    <thead>
            <tr>
                <th>Signal</th>
                <th>Description</th>
                <th>Initial State</th>
                <th>Transition</th>
            </tr>
        </thead>
    
        <tfoot>
            <tr>
                <th>Signal</th>
                <th>Description</th>
                <th>Initial State</th>
                <th>Transition</th>
            </tr>
        </tfoot>
        <tbody>\n\n"""
        f.write(headerFooter)
        for i in range(0, len(remainOneSignals)):
            f.write('        <tr>\n')
            temp = '            <td>'+str(remainOneSignals[i][0])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainOneSignals[i][1])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainOneSignals[i][2])+'</td>\n'
            f.write(temp)
            temp = '            <td>'+str(remainOneSignals[i][3])+'</td>\n'
            f.write(temp)
            f.write('        </tr>\n')
            
        base = """\n\n\n    </tbody>
    </table>\n
    </hhtml>"""
        f.write(base)
        f.close()
    #-------------------------------------------------------------------------------    
    def writeAllSignalTransition(self, allTransQ):
        """Writes all digital signal transitions of each signal

        @summary: This function writes all the transitions of each signal

        @param: allTransQ - List containing all transition of each signal

        @return: None
        """           
        f = open('dig4.html','w')
        headerFooter = """<html>
    
        <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Signal</th>
                    <th>Description</th>
                    <th>Transition</th>
                    <th>Absolute Time</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Signal</th>
                    <th>Description</th>
                    <th>Transition</th>
                    <th>Absolute Time</th>
                </tr>
            </tfoot>
            <tbody>\n\n"""
        f.write(headerFooter)
        for i in range(0, len(allTransQ)):
            f.write('            <tr>\n')
            temp = '                <td>'+str(allTransQ[i][3])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(allTransQ[i][0])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(allTransQ[i][1])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(allTransQ[i][2])+'</td>\n'
            f.write(temp)
            temp = '                <td>'+str(allTransQ[i][4])+'</td>\n'
            f.write(temp)
            f.write('            </tr>\n')
            
        base = """\n        </tbody>
        </table>
        <p></p>
    
    
    </html>"""
        f.write(base)
        f.close()
    #-------------------------------------------------------------------------------
    def peakSignalsHTML(self, sequence, inputData):
        """Writes peaks information of all signal.

        @summary: This function writes peaks of each signal information into Analog1.html file
                  

        @param: sequence - Sequence of writing into file
                  1 - function opens Analog1.html file for writing into it
                  2 - function writes pre-fault and post-fault mean and standard deviation
                  3 - writes all peaks of the signal
                  4 - Writes images of the signal
                  5 - Closes the Analog1.html
                
                inputData - List containing data to be written.

        @return: None
        """           
        
        fileHeader = """<html>
<head>
    <meta charset='utf-8'/>
    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src='../MetroUI/js/jquery.elevatezoom.js'></script> 
</head>\n\n"""
        
        table1Header = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Peak Value</th>
                    <th>Absolute Time</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Peak Value</th>
                    <th>Absolute Time</th>
                </tr>
            </tfoot>
            <tbody>\n"""
        table1Footer = """         </tbody>
        </table>\n"""
        
        table2Header = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th></th>
                    <th>Mean</th>
                    <th>Standard Deviation</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th></th>
                    <th>Mean</th>
                    <th>Standard Deviation</th>
                </tr>
            </tfoot>
            <tbody>\n"""
        table2Footer = """         </tbody>
        </table>
        <p></p>\n"""
        
        fileFooter = """<script>
$("img").elevateZoom({
  zoomType : "lens",
  lensShape : "square",
  lensSize    : 250
});
</script>
</html>"""
        if sequence == 1:
            self.peakSignalFile = open('Analog1.html','w')
            self.peakSignalFile.write(fileHeader)
        if sequence == 2:
            temp = '    <h3>'+inputData[0]+'</h3>\n'
            self.peakSignalFile.write(temp)
            temp = '    <h4>'+ inputData[1]+'</h4>\n'
            self.peakSignalFile.write(temp)
            self.peakSignalFile.write(table2Header)
            self.peakSignalFile.write('                <td><b>Pre Fault</b></td>')
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.peakSignalFile.write(temp)
            temp = '                <td>'+inputData[3]+'</td>\n'
            self.peakSignalFile.write(temp)
            self.peakSignalFile.write('            </tr>\n')     
            self.peakSignalFile.write('                <td><b>Post Fault</b></td>')
            temp = '                <td>'+inputData[4]+'</td>\n'
            self.peakSignalFile.write(temp)
            temp = '                <td>'+inputData[5]+'</td>\n'
            self.peakSignalFile.write(temp)
            self.peakSignalFile.write('            </tr>\n')    
            self.peakSignalFile.write(table2Footer) 
            self.peakSignalFile.write(table1Header)              
        if sequence == 3:
            self.peakSignalFile.write('            <tr>\n')
            temp = '                <td>'+inputData[0]+'</td>\n'
            self.peakSignalFile.write(temp)
            temp = '                <td>'+inputData[1]+'</td>\n'
            self.peakSignalFile.write(temp)        
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.peakSignalFile.write(temp)    
            self.peakSignalFile.write('            </tr>\n')     
        if sequence == 4:
            self.peakSignalFile.write(table1Footer)   
            temp = '    <img src="'+inputData[0]+'" data-zoom-image="'+inputData[1]+'"/>\n\n'
            self.peakSignalFile.write(temp)
        if sequence == 5:
            self.peakSignalFile.write(fileFooter)
            self.peakSignalFile.close()
    #-------------------------------------------------------------------------------
    def nonContinuousSignalsHTML(self, sequence, inputData):
        """Writes non-continuous signal information

        @summary: This function writes non continuous signal information into Analog2.html file.
                  

        @param: sequence - Sequence of writing into file
                  1 - function opens Analog2.html file for writing into it
                  2 - function writes Start time and End time of continuous signal
                  3 - writes maximum aplitude and frequency of the signal
                  4 - Writes images of the signal
                  5 - Closes the Analog2.html
                
                inputData - List containing data to be written.

        @return: None
        """
        fileHeader = """<html>
<head>
    <meta charset='utf-8'/>
    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src='../MetroUI/js/jquery.elevatezoom.js'></script> 
</head>\n\n"""    
        
        tableHeader = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>sequence</th>
                    <th>Frequency</th>
                    <th>Amplitude</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>sequence</th>
                    <th>Frequency</th>
                    <th>Amplitude</th>
                </tr>
            </tfoot>
            <tbody>\n"""
        tableFooter = """        </tbody>
        </table>
        <p></p>\n\n""" 
        
        fileFooter = """<script>
$("img").elevateZoom({
  zoomType : "lens",
  lensShape : "square",
  lensSize    : 250
});
</script>
</html>"""
        
        if sequence == 1:
            self.nonContinuousSignalFile = open('Analog3.html','w')
            self.nonContinuousSignalFile.write(fileHeader)   
        if sequence == 2:
            #Write into HTML file
            temp = '    <h3>'+inputData[0]+'</h3>\n'
            self.nonContinuousSignalFile.write(temp)
            temp = '    <h4>'+ inputData[1]+'</h4>\n'
            self.nonContinuousSignalFile.write(temp)
            temp = '<p><b>Start Time:</b>'+inputData[2]+'      '+'<b>End Time:</b>'+inputData[3]+'</p>\n'
            self.nonContinuousSignalFile.write(temp)        
            self.nonContinuousSignalFile.write(tableHeader)       
        if sequence == 3:
            self.nonContinuousSignalFile.write('            <tr>\n')
            temp = '                <td>'+inputData[0]+'</td>\n'
            self.nonContinuousSignalFile.write(temp)
            temp = '                <td>'+inputData[1]+'</td>\n'
            self.nonContinuousSignalFile.write(temp)
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.nonContinuousSignalFile.write(temp)   
            self.nonContinuousSignalFile.write('            </tr>\n')  
        if sequence == 4:
            self.nonContinuousSignalFile.write(tableFooter)
            temp = '    <img src="'+inputData[0]+'" data-zoom-image="'+inputData[1]+'"/>\n\n'
            self.nonContinuousSignalFile.write(temp)
        if sequence == 5:
            self.nonContinuousSignalFile.write(fileFooter)
            self.nonContinuousSignalFile.close()                               
                 
     #-------------------------------------------------------------------------------
    def smoothTransSignalsHTML(self, sequence, inputData):
        """Writes smooth transition information of the signal

        @summary: This function writes smooth transition information into Analog3.html file.
                  

        @param: sequence - Sequence of writing into file
                  1 - function opens Analog3.html file for writing into it
                  2 - function writes signal and signal description.
                  3 - writes percentage of change, absolute time, relative time information
                  4 - Writes images of the signal
                  5 - Closes the Analog2.html
                
                inputData - List containing data to be written.

        @return: None
        """
        fileHeader = """<html>
<head>
    <meta charset='utf-8'/>
    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src='../MetroUI/js/jquery.elevatezoom.js'></script> 
</head>\n\n"""        
        
        tableHeader = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Value</th>
                    <th>percent_change</th>
                    <th>Absolute Time</th>                
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Relative Time [ms]</th>
                    <th>Value</th>
                    <th>percent_change</th>
                    <th>Absolute Time</th> 
                </tr>
            </tfoot>
            <tbody>\n"""
        tableFooter = """        </tbody>
        </table>
        <p></p>\n\n"""
        
        fileFooter = """<script>
$("img").elevateZoom({
  zoomType : "lens",
  lensShape : "square",
  lensSize    : 250
});
</script>
</html>"""
        
        if sequence == 1:
            self.smoothSignalFile = open('Analog2.html','w')
            self.smoothSignalFile.write(fileHeader)  
        if sequence == 2:
            temp = '    <h3>'+inputData[0]+'</h3>\n'
            self.smoothSignalFile.write(temp)
            temp = '    <h4>'+ inputData[1]+'</h4>\n'
            self.smoothSignalFile.write(temp)  
            self.smoothSignalFile.write(tableHeader)    
        if sequence == 3:
            self.smoothSignalFile.write('            <tr>\n')
            temp = '                <td>'+inputData[0]+'</td>\n'
            self.smoothSignalFile.write(temp)
            temp = '                <td>'+inputData[1]+'</td>\n'
            self.smoothSignalFile.write(temp)
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.smoothSignalFile.write(temp)
            temp = '                <td>'+inputData[3]+'</td>\n'
            self.smoothSignalFile.write(temp)
            self.smoothSignalFile.write('            </tr>\n')      
        if sequence == 4:
            self.smoothSignalFile.write(tableFooter) 
            temp = '    <img src="'+inputData[0]+'" data-zoom-image="'+inputData[1]+'"/>\n\n'
            self.smoothSignalFile.write(temp)
        if sequence == 5:
            self.smoothSignalFile.write(fileFooter)
            self.smoothSignalFile.close()                                                         
        
     #-------------------------------------------------------------------------------
    def corrSignalsHTML(self, sequence, inputData):
        """Writes correlation between two signals information

        @summary: This function writes correlation between two signals information into Analog4.html file.
                  

        @param: sequence - Sequence of writing into file
                  1 - function opens Analog4.html file for writing into it
                  2 - function writes signal name, signal description, shift in ms, fault injected in ms and correlation percentage
                  3 - Writes images of the signal
                  4 - Closes the Analog2.html
                
                inputData - List containing data to be written.

        @return: None
        """    
        fileHeader = """<html>
<head>
    <meta charset='utf-8'/>
    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src='../MetroUI/js/jquery.elevatezoom.js'></script> 
</head>\n\n"""          
              
        tableHeader = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Signal Shift [ms]</th>
                    <th>Fault Induced [ms]</th>
                    <th>Correlation_Percent</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Signal Shift [ms]</th>
                    <th>Fault Induced [ms]</th>
                    <th>Correlation_Percent</th>
                </tr>
            </tfoot>
            <tbody>\n\n"""
        tableFooter = """        </tbody>
        </table>
        <p></p>\n"""
        
        fileFooter = """<script>
$("img").elevateZoom({
  zoomType : "lens",
  lensShape : "square",
  lensSize    : 250
});
</script>
</html>"""
                
        if sequence == 1:
            self.corSignalFile = open('Analog4.html','w')
            self.corSignalFile.write(fileHeader) 
        if sequence == 2:
            #Write into HTML file
            temp = '    <h3>'+inputData[0]+'</h3>\n'
            self.corSignalFile.write(temp)
            temp = '    <h4>'+ inputData[1]+'</h4>\n'
            self.corSignalFile.write(temp)        
            self.corSignalFile.write(tableHeader)
            self.corSignalFile.write('            <tr>\n')
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.corSignalFile.write(temp)
            temp = '                <td>'+inputData[3]+'</td>\n'
            self.corSignalFile.write(temp)   
            temp = '                <td>'+inputData[4]+'</td>\n'
            self.corSignalFile.write(temp)
            self.corSignalFile.write('            </tr>\n')
            self.corSignalFile.write(tableFooter)   
        if sequence == 3:
            temp = '    <img src="'+inputData[0]+'" data-zoom-image="'+inputData[1]+'"/>\n\n'
            self.corSignalFile.write(temp)
        if sequence == 4:
            self.corSignalFile.write(fileFooter)
            self.corSignalFile.close()         
            
    #-------------------------------------------------------------------------------
    def summaryCorrSignalsHTML(self, sequence, inputData):
        """Writes summary of correlation between two signals information

        @summary: This function writes summary of correlation between two signals information into SummaryCorrelation.html file.                  

        @param: sequence - Sequence of writing into file
                  1 - function opens SummaryCorrelation.html file for writing into it
                  2 - function writes signal name, difference between correlation shift and fault indiced instant, shift in ms, fault injected in ms and correlation percentage
                  3 - Writes foo
                  4 - Closes the Analog2.html
                
                inputData - List containing data to be written.

        @return: None
        """          
        tableHeader = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th>Signal</th>
                    <th>corrShift-FaultTime [ms]</th>
                    <th>Correlation_Percent</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th>Signal</th>
                    <th>corrShift-FaultTime [ms]</th>
                    <th>Correlation_Percent</th>
                </tr>
            </tfoot>
            <tbody>\n\n"""
        tableFooter = """        </tbody>
    </table>
    <p> </p>\n"""
                
        if sequence == 1:
            self.summaryCorrFile = open('SummaryCorrelation.html','w')
            self.summaryCorrFile.write('<html>\n') 
            self.summaryCorrFile.write(tableHeader)
        if sequence == 2:
            #Write into HTML file
            self.summaryCorrFile.write('            <tr>\n')
            temp = '                <td>'+inputData[0]+'</td>\n'
            self.summaryCorrFile.write(temp)
            temp = '                <td>'+inputData[1]+'</td>\n'
            self.summaryCorrFile.write(temp)   
            temp = '                <td>'+inputData[2]+'</td>\n'
            self.summaryCorrFile.write(temp)
            self.summaryCorrFile.write('            </tr>\n')
        if sequence == 3:
            self.summaryCorrFile.write(tableFooter)
            self.summaryCorrFile.write('</html>\n')
            self.summaryCorrFile.close()
    #-------------------------------------------------------------------------------
    def commFailHTML(self, sequence, inputData):
        """Writes Commuation Fail related information

        @summary: This function will write captured data for commuation Fail 
                  into Analog5.html file.
                

        @param: sequence - Sequence of writing into file
                  1 - function opens Analog5.html file for writing into it
                  2 - function writes Instance, Time(ms) and Threshold values for start and end instances  
                  3 - Writes images of the signal
                  4 - Closes the Analog5.html
                
                inputData - List containing data to be written.

        @return: None
        """    
        fileHeader = """<html>
<head>
    <meta charset='utf-8'/>
    <script src="../MetroUI/js/jquery-2.1.3.min.js"></script>
    <script src='../MetroUI/js/jquery.elevatezoom.js'></script> 
</head>\n\n"""          
              
        tableHeader = """    <table id="First Transition" class="dataTable striped border bordered" data-role="datatable" data-searching="true">
            <thead>
                <tr>
                    <th></th>
                    <th>Instance</th>
                    <th>Time(ms)</th>
                    <th>Threshold</th>
                </tr>
            </thead>
    
            <tfoot>
                <tr>
                    <th></th>
                    <th>Instance</th>
                    <th>Time(ms)</th>
                    <th>Threshold</th>
                </tr>
            </tfoot>
            <tbody>\n\n"""
        tableFooter = """        </tbody>
    </table>\n"""
        
        fileFooter = """<script>
$("img").elevateZoom({
  zoomType : "lens",
  lensShape : "square",
  lensSize    : 250
});
</script>
</html>"""
                
        if sequence == 1:
            self.commFailFile = open('Analog5.html','w')
            self.commFailFile.write(fileHeader) 
        if sequence == 2:
            #Write into HTML file
            temp = '    <h3>'+ inputData[0] + " for set:"+ inputData[7] +'</h3>\n'
            self.commFailFile.write(temp)
            self.commFailFile.write(tableHeader)
            self.commFailFile.write('                <td><b>Commfail Start</b></td>')
            temp = '                <td>'+str(inputData[1])+'</td>\n'
            self.commFailFile.write(temp)
            temp = '                <td>'+str(inputData[3])+'</td>\n'
            self.commFailFile.write(temp)
            temp = '                <td>'+str(inputData[5])+'</td>\n'
            self.commFailFile.write(temp)
            self.commFailFile.write('            </tr>\n') 
            self.commFailFile.write('                <td><b>Commfail End</b></td>')
            temp = '                <td>'+str(inputData[2])+'</td>\n'
            self.commFailFile.write(temp)
            temp = '                <td>'+str(inputData[4])+'</td>\n'
            self.commFailFile.write(temp)
            temp = '                <td>'+str(inputData[6])+'</td>\n'
            self.commFailFile.write(temp)
            self.commFailFile.write('            </tr>\n')
            self.commFailFile.write(tableFooter)   
        if sequence == 3:
            temp = '    <img src="'+inputData[0]+'" data-zoom-image="'+inputData[1]+'"/>\n\n'
            self.commFailFile.write(temp)
        if sequence == 4:
            #Write into HTML file
            temp = '    <h5>'+ inputData[0] + inputData[1]+'</h5>\n'
            self.commFailFile.write(temp)
        if sequence == 5:
            self.commFailFile.write(fileFooter)
            self.commFailFile.close()       