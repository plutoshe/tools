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
        self.Layerout = {
            "Source":    {"x": 0,    "y": 0, "deltaY": 200, "deltaX": 0, "OffsetX": 50, "OffsetY": 20},
            "Pool":      {"x": 300,  "y": 0, "deltaY": 200, "deltaX": 0, "OffsetX": 60, "OffsetY": 60},
            "Gate":      {"x": 600,  "y": 0, "deltaY": 200, "deltaX": 0, "OffsetX": 60, "OffsetY": 60},
            "Register":  {"x": 900,  "y": 0, "deltaY": 200, "deltaX": 0, "OffsetX": 60, "OffsetY": 60},
            "Convertor": {"x": 1200, "y": 0, "deltaY": 200, "deltaX": 0, "OffsetX": 60, "OffsetY": 60},
        }
        self.Attribute = {
            "Convertor":
            ["ID", "Label", "Geometry", "Style", "Activation", "Activation Mode",
            "Resources (color)", "Show in chart"],
            "ResourceConnection":
            ["ID", "Label", "Geometry", "Style", "Source", "Target", "Transfer", "Color Coding",
            "Color Coding (color)", "Shuffle Source", "Limits (minimum)", "Limits (maximum)"]
        }
        self.CurrentID = 4
        self.AddSource("Common_Source")
        self.AddPool("Nothing")
        
        # self.defaultSourceAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultPoolAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultConvertorAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultGateAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}
        # self.defaultRegisterAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"48.5","as":"offset"}}}
        # self.defaultResourceConnectionAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}
        # self.defaultStaeConnectionAttr = {"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"220","y":"570","as":"sourcePoint"}},{"_attributes":{"x":"304.8528137423857","y":"510","as":"targetPoint"}},{"_attributes":{"x":"20","y":"10","as":"offset"}}]}

    def GetNode(self, i_name):
        if i_name in self.Node:
            return self.Node[i_name]
        return {}

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

    def AddCondition(self, conds, condName, target):
        condID = 0
        for condFrom in conds:
            condID+=1
            #print(condName, i_out[dstName]["Condition"][condName])
            self.AddPool(condName)
            self.StateConnect(condName + str(condID), condFrom, target, conds[condFrom])
                    

    def AddConversion(self, i_conversionName, option, i_in, i_out):
        currentGate = i_conversionName + "_Gate"
        currentConvertor = i_conversionName + "_Convertor"
        
        self.AddGate(currentGate)
        ConvertorOption = {}
        resourceOption = {}
        if "Setting" in option:
            if "Convertor" in option["Setting"]:
                for additionOption in self.Attribute["Convertor"]:
                    if additionOption in option["Setting"]["Convertor"]:
                        ConvertorOption[additionOption] = option["Setting"]["Convertor"][additionOption]
            if "ResourceConnection" in option["Setting"]:
                for additionOption in self.Attribute["ResourceConnection"]:
                    if additionOption in option["Setting"]["ResourceConnection"]:
                        resourceOption[additionOption] = option["Setting"]["ResourceConnection"][additionOption]

        # print(ConvertorOption)
        self.AddConvertorWithOption(currentConvertor, ConvertorOption)

        if "Condition" in option:
            self.AddCondition(option["Condition"], currentGate + "_Condition", currentConvertor)
        
        outSum = 0
        if not i_out:
            return
        else:
            for dstName in i_out:
                self.AddPool(dstName)
                if type(i_out[dstName]) is int:
                    self.ResourceConnectWithOption(i_conversionName + "_" + dstName + "_Connection",  currentGate, dstName, i_out[dstName], resourceOption)
                    outSum += int(i_out[dstName])
                else:
                    outSum += int(i_out[dstName]["value"])
                    if "Condition" in i_out[dstName]:
                        outGate = i_conversionName + "_" + dstName + "_Gate"
                        self.AddGate(outGate)

                        # only or condition support right now
                        # print(i_out)
                        # print(i_out[dstName]["Condition"])
                        self.AddCondition(i_out[dstName]["Condition"], currentGate + "_" + dstName+"_Condition", dstName)

                        #print("outGate", outGate, dstName)
                        # print(i_out[dstName]["value"])
                        self.ResourceConnectWithOption(i_conversionName + "_" + dstName + "_Gate_Connection1", currentGate, outGate, i_out[dstName]["value"], resourceOption)
                        self.ResourceConnectWithOption(i_conversionName + "_" + dstName + "_Gate_Connection2", outGate, "Nothing", "0", resourceOption)
                        self.ResourceConnectWithOption(i_conversionName + "_" + dstName + "_Gate_Connection3", outGate, dstName, i_out[dstName]["value"], resourceOption)
                    else:
                        # print(i_out[dstName]["value"])
                        self.ResourceConnectWithOption(i_conversionName + "_" + dstName + "_Connection",  currentGate, dstName, int(i_out[dstName]["value"]), resourceOption)

        if not i_in:
            self.ResourceConnectWithOption("CommonSource_" + i_conversionName +"_Connection", "Common_Source", currentConvertor, 1, resourceOption)
        else:
            for srcName in i_in:
                self.AddPool(srcName)
                if type(i_in[srcName]) is dict:
                    self.ResourceConnectWithOption(srcName + "_" + i_conversionName +"_Connection", srcName, currentConvertor, i_in[srcName]["value"], resourceOption)
                else:
                    self.ResourceConnectWithOption(srcName + "_" + i_conversionName +"_Connection", srcName, currentConvertor, i_in[srcName], resourceOption)
        self.ResourceConnectWithOption(i_conversionName +"_Connection", currentConvertor, currentGate, outSum, resourceOption)                    
        for dstName in i_out:        
            if type(i_out[dstName]) is dict and "Addition" in i_out[dstName]:
                additionID = 0
                for additionKey in i_out[dstName]["Addition"]:
                    additionID+=1
                    self.StateConnect(i_conversionName + "_" + dstName + "_Addition" + str(additionID), additionKey, i_conversionName + "_" + dstName + "_Connection", i_out[dstName]["Addition"][additionKey])         
                    additionID+=1
                    self.StateConnect(i_conversionName + "_" + dstName + "_Addition" + str(additionID), additionKey, i_conversionName +"_Connection", i_out[dstName]["Addition"][additionKey])         
        
        

    def HasNode(self, i_name):
        
        return i_name in self.Node

    def ResourceConnectWithOption(self, i_name, i_from, i_to, i_num, i_option):
        self.CurrentID += 1
        if not self.HasNode(i_from):
            print("ResourceConnect Failed: graph node doesn't have " + i_from + "!")
        if not self.HasNode(i_to):
            print("ResourceConnect Failed: graph node doesn't have " + i_to + "!")
        self.Node[i_name] = {"ID": self.CurrentID, "type" : "ResourceConnection", "Label":i_num, "Source":i_from, "Target":i_to}
        self.Node[i_name].update(i_option)

    def ResourceConnect(self, i_name, i_from, i_to, i_num):
        self.ResourceConnectWithOption(i_name, i_from, i_to, i_num, {})

    def StateConnect(self, i_name, i_from, i_to, i_label):
        self.CurrentID += 1
        if not self.HasNode(i_from):
            print("StateConnect Failed: graph node doesn't have " + i_from + "!")
        if not self.HasNode(i_to):
            print("StateConnect Failed: graph node doesn't have " + i_to + "!")
        self.Node[i_name] = {"ID": self.CurrentID, "type" : "StateConnection", "Label":i_label, "Source":i_from, "Target":i_to}

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
        #OutputID = self.CurrentID
        for i in self.Node:
            OutputDict[self.Node[i]["type"]][i] = self.Node[i]
        # for i in self.Connection:
        #     #OutputID+=1
        #     OutputDict[self.Connection[i]["type"]][i] = self.Connection[i]
        #     #OutputDict[self.Connection[i]["type"]][i].update({"ID": OutputID})
        with open(i_filepath, mode='wb') as outputFile:
            csvWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csvWriter.writerow(["SOURCES"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Resources (color)", "Show in chart"])

            for i in OutputDict["Source"]:
                v = OutputDict["Source"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=source-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                csvWriter.writerow([v["ID"], i, geometry, style, "passive", "Black", 0])


            # POOL
            csvWriter.writerow([""])
            csvWriter.writerow(["POOLS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Activation", "Activation Mode", "Resources",
            "Resources (color)", "Capacity (limit)", "Capacity (display)", "Overflow", "Show in chart"])
            for i in OutputDict["Pool"]:
                v = OutputDict["Pool"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=pool-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                resources = v["Resources"] if "Resources" in v else 0
                activation = v["Activation"] if "Activation" in v else 'passive'
                activationMode = v["Activation Mode"] if "Activation Mode" in v else "push-any"
                csvWriter.writerow([v["ID"], i, geometry, style, activation, activationMode, resources, "Black", -1, 100, "block", 0])
                
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
            csvWriter.writerow(self.Attribute["Convertor"])

            for i in OutputDict["Convertor"]:
                v = OutputDict["Convertor"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=converter-shape;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                activation = v["Activation"] if "Activation" in v else "interactive"
                activationMode = v["Activation Mode"] if "Activation Mode" in v else "pull-all"
                csvWriter.writerow([v["ID"], i, geometry, style, activation, activationMode, "Black", 0])

            # REGISTER
            csvWriter.writerow([""])
            csvWriter.writerow(["REGISTERS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Interactive", "Limits (minimum)", "Limits (maximum)", "Value (initial)",
            "Value (step)", "Show in chart"])

            for i in OutputDict["Register"]:
                v = OutputDict["Register"][i]
                geometry = '{"_attributes":{"x":"' + str(v["posX"]) + '","y":"' + str(v["posY"]) + '","width":"60","height":"60","TRANSLATE_CONTROL_POINTS":"1","relative":"0","as":"geometry"},"mxPoint":{"_attributes":{"x":"0","y":"40","as":"offset"}}}'
                style = 'shape=register;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;resizable=0;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                # currently not support label things for register
                label = ""
                interactive = 0
                value = v["Value (initial)"] if "value" in v else 0
                csvWriter.writerow([v["ID"], label, geometry, style, interactive, -9999, 9999, 0, 1, value])

            # RESOURCE CONNECTIONS
            # ID	Label	Geometry	Style	Source	Target	Transfer	Color Coding	Color Coding (color)	Shuffle Source	Limits (minimum)	Limits (maximum)														
            # for i in OutputDict["ResourceConnection"]:
            csvWriter.writerow([""])
            csvWriter.writerow(["RESOURCE CONNECTIONS"])
            csvWriter.writerow(self.Attribute["ResourceConnection"])

            for i in OutputDict["ResourceConnection"]:
                v = OutputDict["ResourceConnection"][i]
                source = self.GetNode(v["Source"])
                target = self.GetNode(v["Target"])

                geometry = '{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":' + \
                    '[{"_attributes":{"x":"' + \
                    str(source["posX"] + self.Layerout[source["type"]]["OffsetX"]) + '","y":"' + \
                    str(source["posY"] + self.Layerout[source["type"]]["OffsetY"]) + \
                    '","as":"sourcePoint"}},' + \
                    '{"_attributes":{"x":"' + \
                    str(target["posX"] + self.Layerout[target["type"]]["OffsetX"]) + '","y":"' + \
                    str(target["posY"] + self.Layerout[target["type"]]["OffsetY"]) + \
                    '","as":"targetPoint"}},' + \
                    '{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}'
                style = 'shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;entryX=0;entryY=0.5;entryPerimeter=0;exitX=0.75;exitY=0.5;exitPerimeter=0;'
                #'shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;'
                
                Label = v["Label"]
                ID = v["ID"]
                SourceID = source["ID"]
                TargetID = target["ID"]
                Transfer = v["Transfer"] if "Transfer" in v else "interval-based"
                self.Node[i]["posX"] = (source["posX"] + self.Layerout[source["type"]]["OffsetX"] + target["posX"] + self.Layerout[target["type"]]["OffsetX"]) / 2.0
                self.Node[i]["posY"] = (source["posY"] + self.Layerout[source["type"]]["OffsetY"] + target["posY"] + self.Layerout[target["type"]]["OffsetY"]) / 2.0
                # 4	2	{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}	shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;	8	5	interval-based	0	Black	0	-9999	9999														
                csvWriter.writerow([ID, Label, geometry, style, SourceID, TargetID, Transfer, 0, "Black", 0, -9999, 9999])

            # STATE CONNECTIONS
            # ID	Label	Geometry	Style	Source	Target	Color Coding	Color Coding (color)																		
            csvWriter.writerow([""])
            csvWriter.writerow(["STATE CONNECTIONS"])
            csvWriter.writerow(["ID", "Label", "Geometry", "Style", "Source", "Target", "Color Coding",
            "Color Coding (color)"])
            for i in OutputDict["StateConnection"]:
                v = OutputDict["StateConnection"][i]
                source = self.GetNode(v["Source"])
                target = self.GetNode(v["Target"])
                print("==============")
                print(v["Source"])
                print(v["Target"])
                print(source)
                print(target)
                geometry = '{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":' + \
                    '[{"_attributes":{"x":"' + \
                    str(source["posX"] ) + '","y":"' + \
                    str(source["posY"] ) + \
                    '","as":"sourcePoint"}},' + \
                    '{"_attributes":{"x":"' + \
                    str(target["posX"] ) + '","y":"' + \
                    str(target["posY"]) + \
                    '","as":"targetPoint"}},' + \
                    '{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}'
                # style = 'shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;'
                style = 'shape=state-connection;endArrow=classic;dashed=1;dashPattern=4 3;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;'
                Label = v["Label"]
                ID = v["ID"]
                SourceID = source["ID"]
                TargetID = target["ID"]
                # 4	2	{"_attributes":{"x":"0","y":"0","width":"60","height":"60","relative":"1","TRANSLATE_CONTROL_POINTS":"1","as":"geometry"},"mxPoint":[{"_attributes":{"x":"260","y":"220","as":"sourcePoint"}},{"_attributes":{"x":"345","y":"220","as":"targetPoint"}},{"_attributes":{"x":"-10","y":"10","as":"offset"}}]}	shape=resource-connection;endArrow=classic;html=1;strokeWidth=2;fontSize=16;fontColor=#000000;strokeColor=#000000;exitX=0.75;exitY=0.5;exitPerimeter=0;entryX=0.25;entryY=0.75;entryPerimeter=0;	8	5	interval-based	0	Black	0	-9999	9999														
                csvWriter.writerow([ID, Label, geometry, style, SourceID, TargetID, 0, "Black"])



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
OperationList = ["TwoResourceSelectionOp",
                "OneClayOp",
                "OneReedOp",
                "OneWoodOp",
                "ThreeWoodOp",
                "PlowFieldOp",
                "BuyPatureOp",
                "SowOp",
                "OneGrainOp",
                "OneSheepOp",
                "OneFoodOp",
                "FirstHandOp",
                "Round1Op",
                "Round2Op",
                "Round3Op",
                "Round4Op",
                "Round5Op",
                "Round6Op",
                "Round7Op",
                "Round8Op",
                "Round9Op",
                "Round10Op",
                "Round11Op",
                "Round12Op",
                "Round13Op",
                "Round14Op"]

ListIdentifier = "List"
for playerName in playerList:
    gameobjects[playerName] = gameobject(playerName)

initialResource = {
    "Common":{
        #Operations
        "Round": 0,
        "TwoResourceSelectionOp_Free":1,
        "OneClayOp_Free":1,
        "OneReedOp_Free":1,
        "OneWoodOp_Free":1,
        "ThreeWoodOp_Free":1,
        "PlowFieldOp_Free":1,
        "BuyPatureOp_Free":1,
        "SowOp_Free":1,
        "OneGrainOp_Free":1,
        "OneSheepOp_Free":1,
        "OneFoodOp_Free":1,
        "FirstHandOp_Free":1,
        "Round1Op_Free":1,
        "Round2Op_Free":1,
        "Round3Op_Free":1,
        "Round4Op_Free":1,
        "Round5Op_Free":1,
        "Round6Op_Free":1,
        "Round7Op_Free":1,
        "Round8Op_Free":1,
        "Round9Op_Free":1,
        "Round10Op_Free":1,
        "Round11Op_Free":1,
        "Round12Op_Free":1,
        "Round13Op_Free":1,
        "Round14Op_Free":1,
        "TwoResourceSelectionOp_Used":0,
        "OneClayOp_Used":0,
        "OneReedOp_Used":0,
        "OneWoodOp_Used":0,
        "ThreeWoodOp_Used":0,
        "PlowFieldOp_Used":0,
        "BuyPatureOp_Used":0,
        "SowOp_Used":0,
        "OneGrainOp_Used":0,
        "OneSheepOp_Used":0,
        "OneFoodOp_Used":0,
        "FirstHandOp_Used":0,
        "Round1Op_Used":0,
        "Round2Op_Used":0,
        "Round3Op_Used":0,
        "Round4Op_Used":0,
        "Round5Op_Used":0,
        "Round6Op_Used":0,
        "Round7Op_Used":0,
        "Round8Op_Used":0,
        "Round9Op_Used":0,
        "Round10Op_Used":0,
        "Round11Op_Used":0,
        "Round12Op_Used":0,
        "Round13Op_Used":0,
        "Round14Op_Used":0,
        "RoundFinish_Op": 0,
    },
    "Player":{
       ListIdentifier: playerList,
       "AvailablePeople": 2,
    }
}

builders = {
    "RoundFinish":
    {
        "in":{},
        "out":{
            "Common":{
                "RoundFinish_Resource": 1,
                "RoundFinish_Op": 1,
                "Round": 1,
            }
        }
    },
    "RoundFinish_Resource":
    {
        "Setting":
        {"Convertor":{"Activation":"automatic"}},
        
        "in" : {
            "Common":{
                "RoundFinish_Resource":1,
            }
        },
        "out" : {
            "Common" : {
                "OneReed": 1,
                "OneWood": 1,
                "ThreeWood": 3,
                "OneGrain": 1,
                "OneSheep": 1,
                "OneFood": 1,
                "OneFirstHandFood": 1,
                "OneClay": 1,
                "OneBoar": {"value" : 1, "Condition": {"Common_Round": ">6"}},
                "OneCastle": {"value": 1, "Condition": {"Common_Round": ">8"}},
            },
        },
    },
    
    # "OneClayOp":
    # {
    #     "in":{
    #         "Common":{"OneClayOp_Free":1},
    #     },
    #     "Out":{
    #         "Common":{
    #             "OneClayOp_Used":1,
    #             "OneClay_TransferResource":1,
    #         }
    #     }
    # }

    # "PlayerRound":
    # {
        
    #         "in": {"Player": {"UnavailablePeople": "all"}},
    #         "out": {"Player": {"AvailablePeople": "all"}},
    #     }
    # }
    "CommonRoundOperation":
    {
        ListIdentifier: OperationList,
        "Setting":
        {
            "Convertor":{"Activation":"automatic"},
            "ResourceConnection":{"Transfer": "instantaneous"},
        },
   
        "Condition": {'Common_RoundFinish_Op': ">0"},
        #"Condition": {'RoundFinish_Op': ">0"},
        "in":{ "Common" : {
            "Used": {ListIdentifier: True, "value": 1}, 
        }},
        "out": {"Common": {"Free": {ListIdentifier: True, "value": 1}}},
        
    },
    "RoundFinish_Op":
    {
        "Setting":
        {
            "Convertor":{"Activation":"automatic"},
        },
        "in" : {
            "Common":{
                "RoundFinish_Op": 1,
            }
        },
        "out": {
            "Common":{
                "RoundFinish_Op_Used": 1,
            },
        }
    },
    "PlayerOneClayOp":
    {
        "Setting":
        {
            "ResourceConnection":{"Transfer": "instantaneous"},
        },
        ListIdentifier: playerList,
        "in":{
            "Common": {
                "OneClayOp_Free": 1,
            },
            
        },
        "out":{
            "Common": {
                "OneClayOp_Used": 1,
            },
            "": { 
                "Clay": {
                    ListIdentifier: True,
                    "Addition": {"Common_OneClay": "+1"},
                    "value": 0,
                },
            }
        },
    },
    "CommonOneClayClean":
    {
        "Setting":
        {
            "Convertor":{"Activation":"automatic"},
        },
        "Condition": { "Common_OneClayOp_Used":">0"},
        "in":{
            "Common": {
                "OneClay":"all",
            },
        },
        "out":{
            "": {
                "Nothing": 0,
            }
        }
    }
}


graph = machinationGraph()
# for obj in gameobjects:
#     for r in gameobjects[obj].resourceList:
#         graph.AddPoolWithOption(obj +"_"+ r, {"Resources" : gameobjects[obj].resourceList[r]})

for ResourceKey in initialResource:
    element = initialResource[ResourceKey]
    if ListIdentifier in element:
        for unit in element[ListIdentifier]:
            for i in element:
                if i != ListIdentifier:
                    graph.AddPoolWithOption(unit + "_" + i, {"Resources": element[i]})
    else:
        for i in element:
            graph.AddPoolWithOption(ResourceKey + "_" + i, {"Resources": element[i]})
            # print(ResourceKey + "_" + i)

for builderKey in builders:
    element = builders[builderKey]
    if ListIdentifier in element:
        # print(element)
        for unit in element[ListIdentifier]:
            srcList = {}
            dstList = {}
            for i in element["in"]:
                for k in element["in"][i]:
                    Prefix = i + "_" if i != "" else ""
                    if type(element["in"][i][k]) is dict and ListIdentifier in element["in"][i][k]:
                        srcList[Prefix + unit + "_" + k] = element["in"][i][k]
                    else:
                        srcList[Prefix + k] = element["in"][i][k]
            for i in element["out"]:
                for k in element["out"][i]:
                    Prefix = i + "_" if i != "" else ""
                    if type(element["out"][i][k]) is dict and ListIdentifier in element["out"][i][k]:
                        dstList[Prefix + unit + "_" + k] = element["out"][i][k]
                    else:
                        dstList[Prefix + k] = element["out"][i][k]
            graph.AddConversion(unit + "_" + builderKey, element, srcList, dstList)
    else:
        srcList = {}
        dstList = {}
        for i in element["in"]:
            Prefix = i + "_" if i != "" else ""
            for k in element["in"][i]:
                srcList[Prefix + k] = element["in"][i][k]
        for i in element["out"]:
            Prefix = i + "_" if i != "" else ""
            for k in element["out"][i]:
                dstList[Prefix + k] = element["out"][i][k]
        graph.AddConversion(builderKey, element, srcList, dstList)
    # if "Common" in builders[aBuilder]["in"]:
    #     for i in builders[aBuilder]["in"]["Common"]:
    #         srcList["Common_" + i] = builders[aBuilder]["in"]["Common"][i]
    # if "Common" in builders[aBuilder]["out"]:
    #     for i in builders[aBuilder]["out"]["Common"]:
    #         dstList["Common_" + i] = builders[aBuilder]["out"]["Common"][i]
    # if "Player" in builders[aBuilder]["in"] or "Player" in builders[aBuilder]["out"]:
    #     for playerName in playerList:
    #         specialSrcList = srcList
    #         specialDstList = dstList
    #         if "Player" in builders[aBuilder]["in"]:
    #             for i in builders[aBuilder]["in"]["Player"]:
    #                 specialSrcList[playerName + "_" + i] = builders[aBuilder]["in"]["Player"][i]
    #         if "Player" in builders[aBuilder]["out"]:
    #             for i in builders[aBuilder]["out"]["Player"]:
    #                 specialDstList[playerName + "_" + i] = builders[aBuilder]["out"]["Player"][i]
    #         graph.AddConversion(playerName + "_" + aBuilder, specialSrcList, specialDstList)
    # else:
    #     graph.AddConversion(aBuilder, srcList, dstList)

graph.OutputToCsv("a.csv")
    