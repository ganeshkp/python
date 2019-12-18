#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created By: Ganeshkumar patil
Date: 23-Oct-2019
Description: This file reads APEX log file and provides filtered signal with full path.
Ex. Call getPathList() with first parameter with signal name and remaining as filtering parameters
    like apex path node name. You can specify any number of filtering parameters for this function.
"""

import itertools, os
SKIP_JUNK_DATA=0

import sys, json

dpgJsContent="""var plotDataList=[];
// Plotly functions
function plotGraph(plotDataList){
    var data=[];
    trace={};
    for (i=0; i<plotDataList.length;i++){
        var trace={mode:"lines", x:plotDataList[i].xData, y:plotDataList[i].yData, name:plotDataList[i].signal, line:{width:2}};
        data.push(trace);
    }
    var layout={title:"Signal Data Trend", 
                autosize:true,
                xaxis:{title:'sample', automargin:true, zeroline:true, showgrid:true, showline:true, mirror:'ticks',
                  gridcolor:'#bdbdbd', gridwidth:1, zerolinecolor:'#969696', zerolinewidth:3, linecolor: '#636363', 
                  linewidth: 3}, 
                yaxis:{title:"value", automargin:true, zeroline:true, showgrid:true, showline:true, mirror:'ticks',
                  gridcolor:'#bdbdbd', gridwidth:1, zerolinecolor:'#969696', zerolinewidth:3, linecolor: '#636363', 
                  linewidth: 3}                
               };
    return [data, layout];
}

function range(start, end) {
    var total = [];
    if (!end) {
        end = start;
        start = 0;
    }
    for (var i = start; i < end; i += 1) {
        total.push(i);
    }
    return total;
}

function getTreeData(){
    return treeData;
}\n\n"""

indexFileContent="""<!-- <!DOCTYPE html> -->
<head>
    <title>Datapoint Graph</title>
    <!--LINK WEBIX -->
    <script type="text/javascript" src="common/webix.js?v=6.4.5"></script>
    <link rel="stylesheet" type="text/css" href="common/webix.css?v=6.4.5">
    <!-- LINK DPG FILES -->
    <link rel="stylesheet" type="text/css" href="common/dpgStyle.css">
    <script src='dpg.js'></script>
    <!-- LINK PLOTLY -->
    <script src='common/plotly-latest.min.js'></script>
</head>
<body>
    <div id="TREE_LOCATION" style="height:95vh;"></div>
    <div id="GRAPH_LOCATION"></div>

    <script type="text/javascript" charset="utf-8">    

        webix.ready(function(){
             //loading from file
            webix.ui({
                    type:"space",
                    margin:2,
                    padding:0,
                    autowidth:false,
                    container:"TREE_LOCATION",
                    rows:[
                        {
                            view:"toolbar", 
                            height: 50,
                            cols:[
                                // { gravity:5 },
                                {template:"<div class='header_comment'>Data Point Graph</div>"},
                            ]
                        },
                            
                        {view:"resizer"},
                        {
                            cols:[
                            {
                                view:"tree",
                                width:400,
                                drag:"source",
                                select:true,
                                url:function(params){
                                    return getTreeData();
                                },
                                // data:treeData,
                                on: {
                                    onBeforeDrag: function(context) {
                                      let id = context.start;
                                      const path = [id];
                                      
                                      while (id = this.getParentId(id)){
                                        path.unshift(id);
                                      }
                                 
                                      let fullPath = path.map((id) => {
                                        return this.getItem(id).value;
                                      }).join("/");
                                 
                                      //webix.message(`Full path: ${fullPath}`);
                                      context.path = fullPath;
                                    }
                                }
                            },
                            {view:"resizer"},
                            {
                                view:"template",
                                autoheight:true,
                                id:"plotPage",
                                content:"GRAPH_LOCATION",
                            }]
                    }]
            });
            webix.DragControl.addDrop("GRAPH_LOCATION", {
                $drop:function(source, target, event){
                    var dnd = webix.DragControl.getContext();
                    path="/"+dnd.path;
                    
                    basename=path.split("/").pop();
                    var isPltExists=false;
                    for (var i=0; i<plotDataList.length; i++){
                        if (plotDataList[i].signal==basename){
                            isPltExists=true;
                            webix.message("Signal already exists");
                            break
                        }
                    }

                    if (isPltExists == false){
                        sigData={};
                        sigData["signal"]=basename;
                        monId=monIdPathMap[path];
                        
                        sigData["yData"]=monIdData[monId];
                        length=monIdData[monId].length;
                        sigData["xData"]=range(length);
                        plotDataList.push(sigData);

                        //PLOT GRAPH
                        var values=plotGraph(plotDataList);
                        data=values[0];
                        layout=values[1];
                        Plotly.newPlot('GRAPH_LOCATION', data, layout);
                    }
                }
            })
        });
    </script>
</body>
</html>\n\n"""


def parseArgs(args):
    if "-h" in args:
        print(__doc__)
        exit(0)
    if "-f" in args:
        # Get the index of the option
        index = args.index("-f")
        FILE_NAME = args[index + 1]
    else:
        print("Alias file name needs to be provided. please check 'python validateAliasFile.py -h' for help")
        exit(1)

    return FILE_NAME

class ReadRestLog():
    def __init__(self, restFile):
        self.monIdList=[]
        self.aliasList=[]
        self.monIdData={}
        self.monIdPathMap={}
        self.mainDict={}

        self.extractAliasList(restFile)
        self.extractdata(restFile)

    def extractdata(self, restFile):
        try:
            logFile = open(restFile, 'r')
            for line in itertools.islice(logFile, SKIP_JUNK_DATA, None):
                line = line.strip()
                if line.startswith("//"):
                    continue

                # Check for data values
                if line.startswith("#E"):
                    allData = line.split(',')

                    monId = allData[1]
                    if ((allData[6] == ' ') or (allData[7] == ' ')) or \
                            ((allData[6] == "0") and (allData[7] == "0")) or \
                            ((allData[6] == "0.000000") and (allData[7] == "0.000000")):
                        continue
                    elif monId in self.monIdList:
                        if allData[7].isnumeric():
                            self.addToApexDataDict(monId, float(allData[7]))
            logFile.close()
        except Exception as err:
            print(f"Issue in extracting data:{err}")


    def extractAliasList(self, restFile):
        logFile = open(restFile, 'r')
        for line in itertools.islice(logFile, SKIP_JUNK_DATA, None):
            line = line.strip()
            if line.startswith("//"):
                continue
            # Check for data values
            if line.startswith("#A"):
                allData = line.split(',')
                self.monIdList.append(allData[1])
                self.aliasList.append(allData[2])
                self.monIdPathMap[allData[2]]=allData[1]
        logFile.close()

    def addToApexDataDict(self, key, val):
        if key in self.monIdData.keys():
            list1=self.monIdData[key]
        else:
            list1=[]
        list1.append(val)
        self.monIdData[key]=list1

    def getPathList(self, *args):
        finalList=self.aliasList
        sigNamelist=[]
        if len(args) > 0:
            finalList=[]
            for path in self.aliasList:
                if args[0] == os.path.basename(path):
                    sigNamelist.append(path)
            if len(args)==1:
                finalList=sigNamelist
            else:
                for path in sigNamelist:
                    if self.allSubstringInString(list(args), path)==True:
                        finalList.append(path)

        #RETURN FINAL LIST OF PATHS
        return finalList

    def allSubstringInString(self, args, path):
        counter=0
        for substring in args:
            if substring in path:
                counter=counter+1
        if counter==len(args):
            return True
        else:
            return False

    def createDict(self, l, d=dict(), id="1"):
        prevDict1 = {}
        tempId = id.split('.')
        tempId[-1] = str(int(tempId[len(tempId) - 1]) + 1)

        for num in range(len(l), 0, -1):
            id = '.'.join(tempId)
            element = l[num - 1]
            list1 = []
            dict1 = {}
            if num != 1:
                for i in range(1, num):
                    id = id + ".1"
            dict1["id"] = id
            dict1["value"] = element
            list1.append(prevDict1)
            if num != len(l):
                dict1["data"] = list1
            prevDict1 = dict1
            if num == 1:
                return dict1

    def addToDict(self, path):
        l = path.split('/')[1:]

        # CHECK IF EMPTY DICTIONARY
        if len(self.mainDict) == 0:
            prevDict1 = {}
            for num in range(len(l), 0, -1):
                id = "1"
                element = l[num - 1]
                list1 = []
                dict1 = {}
                for i in range(1, num):
                    id = id + ".1"
                dict1["id"] = id
                dict1["value"] = element
                list1.append(prevDict1)
                if num != len(l):
                    dict1["data"] = list1
                prevDict1 = dict1
                if num == 1:
                    self.mainDict = dict1
        else:
            self.parseMainDict(l)

    def parseMainDict(self, l):
        a = self.mainDict
        count = 1
        prevDict = {}
        id = "1"
        try:
            while (len(l) > 0):
                element = l.pop(0)
                if element == a["value"]:
                    prevDict = a
                    element = l.pop(0)
                    for j in range(len(a["data"])):
                        if element == a["data"][j]["value"]:
                            a = a["data"][j]
                            break
                    l.insert(0, element)

                elif len(l) == 0:
                    dict2 = {}
                    list1 = prevDict["data"]
                    if len(list1) == 0:
                        for num in range(len(l) + 1):
                            id = id + ".1"
                    else:
                        temp = list1[len(list1) - 1]
                        tempId = temp["id"].split('.')
                        tempId[-1] = str(int(tempId[len(tempId) - 1]) + 1)
                        id = '.'.join(tempId)
                    dict2["id"] = id
                    dict2["value"] = element
                    list1.append(dict2)
                else:
                    # ADD NEW PATH IF IT DOES NOT EXIST
                    list1 = prevDict["data"]
                    l.insert(0, element)
                    dict3 = self.createDict(l, id=list1[len(list1) - 1]["id"])
                    list1.append(dict3)
                    break
        except Exception as err:
            pass

    def genIndexFile(self):
        for path in self.aliasList:
            self.addToDict(path)

        #GENERATE dpg.js file
        f = open("dpg.js", "w")
        f.write("var treeData=["+json.dumps(self.mainDict)+"];\n")
        f.write("var monIdData="+json.dumps(self.monIdData)+";\n")
        f.write("var monIdPathMap="+json.dumps(self.monIdPathMap)+";\n\n")
        f.write(dpgJsContent)
        f.close()

        #GENERATE index.html file
        f = open("index.html", "w")
        f.write(indexFileContent)
        f.close()
        print("tree data created\n")

if __name__ == "__main__":
    (FILE_NAME) = parseArgs(sys.argv)
    obj1 = ReadRestLog(FILE_NAME)
    obj1.genIndexFile()

    #signal=test1Object.getPathList('Task Error Status','Instance 1','tDmaJobTask')
    #print(signal)
    print("Execution completed\n")
