import csv

resourceNameList = [
    "Sheep", "Boar", "Castle", "Wood", "Reed", "Clay", "Grain",  
    "EmptyField", "ThreeGrainField", "TwoGrainField", "OneGrainField", 
    "Stable",  
    "OneGridPatureNoStable", "TwoGridPatureNoStable", "ThreeGridPatureNoStable", "FourGridPatureNoStable",
    "OneGridPatureWithStable", "TwoGridPatureWithStable", "ThreeGridPatureWithStable", "FourGridPatureWithStable",
    "Room", "Wooden/Clay_Room", "People", "CompletedPeople", "Food", "BeggingMark"]
ImprovementList = {}
commonResource = {}


class machinationGraph:
    # Node = {}
    # Connection = {}
    # CurrentID = 0
        
    def __init__(self):
        # self.Sources = {}
        # self.Pools = {}
        # self.Gates = {}
        # self.Registers = {}
        # self.Convertors = {}
        # self.ResourceConnections = {}
        # self.StateConnections = {}

        self.Node = {}
        self.Connection = {}
        self.Layerout = {
            "Source":    {"x": 0,    "y": 0, "deltaY": 200, "deltaX": 0},
            "Pool":      {"x": 300,  "y": 0, "deltaY": 200, "deltaX": 0},
            "Gate":      {"x": 600,  "y": 0, "deltaY": 200, "deltaX": 0},
            "Register":  {"x": 900,  "y": 0, "deltaY": 200, "deltaX": 0},
            "Convertor": {"x": 1200, "y": 0, "deltaY": 200, "deltaX": 0},
        }
        self.CurrentID = 0
        self.AddSource("Common_Source")
        
        # self.defaultSourceAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultPoolAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultConvertorAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultGateAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultRegisterAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"48.5","as":"offset"}}}
        # self.defaultResourceConnectionAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}
        # self.defaultStateConnectionAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"220","y":"570","as":"sourcePoint"}},{"_attributes":{"x":"304.8528137423857","y":"510","as":"targetPoint"}},{"_attributes":{"x":"20","y":"10","as":"offset"}}]}

    def AddNode(self, i_name, i_type, i_option):
        if i_name not in self.Node:
            self.CurrentID += 1
            self.Node[i_name] = {"type" : i_type, "ID": self.CurrentID, "posX":self.Layerout[i_type]["x"], "posY":self.Layerout[i_type]["y"]}
            self.Layerout[i_type]["x"] += self.Layerout[i_type]["deltaX"]
            self.Layerout[i_type]["y"] += self.Layerout[i_type]["deltaY"]
            self.Node[i_name].update(i_option)
    
    def AddSource(self, i_name):
        self.AddSourceWithOption(i_name, {})

    def AddSourceWithOption(self, i_name, i_option):
        self.AddNode(i_name, "Source", i_option)
        

    def AddPool(self, i_name):
        self.AddPoolWithOption(i_name, {})

    def AddPoolWithOption(self, i_name, i_option):
        self.AddNode(i_name, "Pool", i_option)

    def AddRegister(self, i_name):
        self.AddRegisterWithOption(i_name, {})

    def AddRegisterWithOption(self, i_name, i_option):
        self.AddNode(i_name, "Register", i_option)

    def AddGate(self, i_name):
        self.AddGateWithOption(i_name, {})
        
    def AddGateWithOption(self, i_name, i_option):
        self.AddNode(i_name, "Gate", i_option)

    def AddConvertor(self, i_name):
        self.AddConvertorWithOption(i_name, {})
        
    def AddConvertorWithOption(self, i_name, i_option):
        self.AddNode(i_name, "Convertor", i_option)

    def AddConversion(self, i_conversionName, i_in, i_out):
        currentGate = i_conversionName + "_Gate"
        currentConvertor = i_conversionName + "_Convertor"
        
        self.AddGate(currentGate)
        self.AddConvertor(currentConvertor)
        outSum = 0
        if not i_out:
            return
        else:
            for dstName in i_out:
                self.ResourceConnect(i_conversionName +"_Connection",  currentConvertor, dstName, i_out[dstName])
                outSum += int(i_out[dstName])

        if not i_in:
            self.ResourceConnect(i_conversionName +"_Connection", "Common_Source", currentConvertor, 1)
        else:
            for srcName in i_in:
                self.ResourceConnect(i_conversionName +"_Connection", srcName, currentConvertor, i_in[srcName])
        
        self.ResourceConnect(i_conversionName +"_Connection", currentConvertor, currentGate, outSum)

    def ResourceConnect(self, i_name, i_from, i_to, i_num):
        self.CurrentID += 1
        self.Connection[i_name] = {"ID": self.CurrentID, "type" : "ResourceConnection", "Label":i_num, "Source":self.Node[i_from], "Target":self.Node[i_to]}

    def StateConnect(self, i_name, i_from, i_to, i_label):
        self.CurrentID += 1
        self.Connection[i_name] = {"ID": self.CurrentID, "type" : "StateConnection", "Label":i_label, "Source":self.Node[i_from], "Target":self.Node[i_to]}

    def OutputToCsv(self, i_filepath):
        OutputDict = {
            "Source":{},
            "Pool":{},
            "Register":{},
            "Gate":{},
            "Convertor":{},
            "StateConnection":{},
            "ResourceConnection":{},
        }
        OutputID = self.CurrentID
        for i in self.Node:
            OutputDict[self.Node[i]["type"]][i] = self.Node[i]
        
        for i in self.Connection:
            OutputID+=1
            OutputDict[self.Connection[i]["type"]][i] = self.Connection[i]
            OutputDict[self.Connection[i]["type"]][i].update({"ID": OutputID})
        with open(i_filepath, mode='wb') as outputFile:
            csvWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csvWriter.writerow(["SOURCES"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Resources (color)", "Show in chart"])

            for i in OutputDict["Source"]:
                v = OutputDict["Source"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=source-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                csvWriter.writerow([v["ID"], i, geometry, style, "automatic", "Black", 0])


            # POOL
            csvWriter.writerow([""])
            csvWriter.writerow(["POOLS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Activation Mode	Resources",
            "Resources (color)", "Capacity (limit)", "Capacity (display)", "Overflow", "Show in chart"])
            for i in OutputDict["Pool"]:
                v = OutputDict["Pool"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=pool-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                csvWriter.writerow([v["ID"], i, geometry, style, "passive", "push-any", 0, "Black", -1, 100, "block", 0])
                
            # GATES
            csvWriter.writerow([""])
            csvWriter.writerow(["GATES"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Activation Mode",
            "Distribution", "Show in chart"])
            for i in OutputDict["Gate"]:
                v = OutputDict["Gate"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=gate-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                
                csvWriter.writerow([v["ID"], i, geometry, style,  "passive", "pull-all", "deterministic", 0])

            # CONVERTERS
            csvWriter.writerow([""])
            csvWriter.writerow(["CONVERTERS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Activation Mode",
            "Resources (color)", "Show in chart"])

            for i in OutputDict["Convertor"]:
                v = OutputDict["Convertor"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=converter-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                csvWriter.writerow([v["ID"], i, geometry, style,  "interactive", "pull-all", "Black", 0])

            # REGISTER
            csvWriter.writerow([""])
            csvWriter.writerow(["REGISTER"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Interactive", "Limits (minimum)", "Limits (maximum)", "Value (initial)",
            "Value (step)", "Show in chart"])

            for i in OutputDict["Register"]:
                v = OutputDict["Register"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=register;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                # currently not support label things for register
                label = ""
                interactive = 0
                csvWriter.writerow([v["ID"], label, geometry, style, interactive, -9999, 9999, 0, 1, 0])

            # RESOURCE CONNECTIONS
            # ID	Label	Geometry	Style	Source	Target	Transfer	Color Coding	Color Coding (color)	Shuffle Source	Limits (minimum)	Limits (maximum)														
            # for i in OutputDict["ResourceConnection"]:
            csvWriter.writerow([""])
            csvWriter.writerow(["RESOURCE CONNECTIONS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Source", "Target", "Transfer", "Color Coding",
            "Color Coding (color)", "Shuffle Source", "Limits (minimum)", "Limits (maximum)"])
            for i in OutputDict["ResourceConnection"]:
                v = OutputDict["ResourceConnection"][i]

                geometry = '{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":' + \
                    '[{"_attributes":{"x":"' + \
                    str(v["Source"]["posX"] + 60) + '","y":"' + \
                    str(v["Source"]["posY"] + 60) + \
                    '","as":"sourcePoint"}},' + \
                    '{"_attributes":{"x":"' + \
                    str(v["Target"]["posX"] + 60) + '","y":"' + \
                    str(v["Target"]["posY"] + 60) + \
                    '","as":"targetPoint"}},' + \
                    '{"_attributes":{"x":"-10","\y":"10","as":"offset"}}]}'
                style = 'shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;'
                
                Label = v["Label"]
                ID = v["ID"]
                Source = v["Source"]["ID"]
                Target = v["Target"]["ID"]
                # 4	2	{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}	shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;	8	5	interval-based	0	Black	0	-9999	9999														
                csvWriter.writerow([ID, Label, geometry, style, Source, Target, "interval-based", 0, "Black", 0, -9999, 9999])

            # STATE CONNECTIONS
            # ID	Label	Geometry	Style	Source	Target	Color Coding	Color Coding (color)																		
            csvWriter.writerow([""])
            csvWriter.writerow(["RESOURCE CONNECTIONS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Source", "Target", "Color Coding",
            "Color Coding (color)"])
            for i in OutputDict["StateConnection"]:
                v = OutputDict["ResourceConnection"][i]
                geometry = '{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":' + \
                    '[{"_attributes":{"x":"' + \
                    str(v["Source"]["posX"] + 60) + '","y":"' + \
                    str(v["Source"]["posY"] + 60) + \
                    '","as":"sourcePoint"}},' + \
                    '{"_attributes":{"x":"' + \
                    str(v["Target"]["posX"] + 60) + '","y":"' + \
                    str(v["Target"]["posY"] + 60) + \
                    '","as":"targetPoint"}},' + \
                    '{"_attributes":{"x":"-10","\y":"10","as":"offset"}}]}'
                style = 'shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;'
                Label = v["Label"]
                ID = v["ID"]
                Source = v["Source"]["ID"]
                Target = v["Target"]["ID"]
                # 4	2	{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}	shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;	8	5	interval-based	0	Black	0	-9999	9999														
                csvWriter.writerow([ID, Label, geometry, style, Source, Target, 0, "Black"])



for i in range(11):
    ImprovementList[i] = 0

class resource:
    def __init__(self):
        self.name = ""
        self.value = 0

class gameobject:
    def __init__(self, name):
        self.name = name
        self.resourceList = {}
        for i in resourceNameList:
            self.resourceList[i] = 0

gameobjects = {
    "Common" : gameobject("Common")}
playerList = ["Player1", "Player2"]
for playerName in playerList:
    gameobjects[playerName] = gameobject(playerName)

builders = {
    "CommonSupplyAdd":
    {
        "in" : {},
        "out" : {"Common" : {"Sheep": 1}},
    },
    "HarvestPhase1":
    {
        "in" : {"Player": {"ThreeGrainField": 1}},
        "out" : {"Player": {"TwoGrainField": 1, "Grain": 1}},
    },
    "HarvestPhase2":
    {
        "in" : {"Player": {"ThreeGrainField": 1}},
        "out" : {"Player": {"TwoGrainField": 1, "Grain": 1}},
    },
    # "CompleteRound":
    # {
    #     "in": {"Player" : {"CompletedPeople": "all"}},
    #     "out":{"Player" : {"People" : "all"}},
    # }
}

graph = machinationGraph()
for obj in gameobjects:
    for r in gameobjects[obj].resourceList:
        graph.AddPoolWithOption(obj +"_"+ r, {"Resources" : gameobjects[obj].resourceList[r]})
print(graph)  
for aBuilder in builders:
    srcList = {}
    dstList = {}
    if "Common" in builders[aBuilder]["in"]:
        for i in builders[aBuilder]["in"]["Common"]:
            srcList["Common_" + i] = builders[aBuilder]["in"]["Common"][i]
    if "Common" in builders[aBuilder]["out"]:
        for i in builders[aBuilder]["out"]["Common"]:
            dstList["Common_" + i] = builders[aBuilder]["out"]["Common"][i]
    if "Player" in builders[aBuilder]["in"] or "Player" in builders[aBuilder]["out"]:
        for playerName in playerList:
            specialSrcList = srcList
            specialDstList = dstList
            if "Player" in builders[aBuilder]["in"]:
                for i in builders[aBuilder]["in"]["Player"]:
                    specialSrcList[playerName + "_" + i] = builders[aBuilder]["in"]["Player"][i]
            if "Player" in builders[aBuilder]["out"]:
                for i in builders[aBuilder]["out"]["Player"]:
                    specialDstList[playerName + "_" + i] = builders[aBuilder]["out"]["Player"][i]
            graph.AddConversion(aBuilder, specialSrcList, specialDstList)
    else:
        graph.AddConversion(aBuilder, srcList, dstList)

graph.OutputToCsv("a.csv")
    