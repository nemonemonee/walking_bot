import pybullet as p
import pybullet_data
from world import WORLD
from robot import ROBOT
import time
import constants as c
class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        if directOrGUI ==  "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-50)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        
    def __del__(self):
        p.disconnect()
    
    def Run(self):
        for i in range(c.simulationSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
        self.Get_Fitness()
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()
