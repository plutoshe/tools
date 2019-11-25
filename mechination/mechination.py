
resourceNameList = [
    "Sheep", "Boar", "Castle", "Wood", "Reed", "Clay", "Grain",  
    "EmptyField", "ThreeGrainField", "TwoGrainField", "OneGrainField", 
    "Stable",  
    "OneGridPatureNoStable", "TwoGridPatureNoStable", "ThreeGridPatureNoStable", "FourGridPatureNoStable",
    "OneGridPatureWithStable", "TwoGridPatureWithStable", "ThreeGridPatureWithStable", "FourGridPatureWithStable",
    "Room", "Wooden/Clay_Room", "People", "CompletedPeople", "Food", "BeggingMark"]
ImprovementList = {}
commonResource = {}

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
         
class InteractionBuilder:
    def __init__(self, i_in, i_out):
        self.m_in = i_in
        self.m_out = i_out

class AutomateddBuilder:
    def __init__(self, i_in, i_out):
        self.m_in = i_in
        self.m_out = i_out

players = {
    "Common" : gameobject("Common"), 
    "Player1" : gameobject("Player1"),
    "Player2" : gameobject("Player2")}
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
    "CompleteRound":
    {
        "in": {"Player" : {"CompletedPeople": "all"}},
        "out":{"Player" : {"People" : "all"}},
    }

}