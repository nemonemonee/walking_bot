import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import pickle

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        #numpy.random.seed(id)
        self.InitializeRandomVariables()
        self.BuildBodyPlan()
        self.ArrangementPlan()
        self.abs_pos = numpy.zeros((self.length, 3))
        self.abs_pos[0] = numpy.array([0,0,self.toBotm])
        
    def Evaluate(self):
        self.Start_Simulation()
        self.Wait_For_Simulation_To_End()
    
    def Start_Simulation(self, directOrGUI):
        if self.myID == 0:
            self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        if directOrGUI == "GUI":
            os.system("python3 simulate.py GUI "+str(self.myID))
        else:
            os.system("python3 simulate.py "+directOrGUI+" "+str(self.myID)+" &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness"+str(self.myID)+".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm "+fitnessFileName)
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box0", pos=[-5,0,.2] , size=[5,20,1])
#        for i in range(1,10):
#            pyrosim.Send_Cube(name="Box"+str(i), pos=[-5-5*i,0,.2+.5*i] , size=[5,10,.5+i])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
        pyrosim.Send_Cube(name="0", pos=self.abs_pos[0], size=self.size[0], colorName=self.GetColor(0)[0], colorString=self.GetColor(0)[1])
        allDir = {0:numpy.array([1,0,0]), 1:numpy.array([0,1,0]), 2:numpy.array([0,0,1]),
                  3:numpy.array([0,0,-1]), 4:numpy.array([0,-1,0]), 5:numpy.array([-1,0,0])}

        for j in self.bodyPlan[0]:
            center2pivot = allDir[self.growDir[j]]
            self.abs_pos[j] = self.abs_pos[0]+center2pivot*.5*(self.size[0]+self.size[j])
            ball = "m0" + str(j)
            pyrosim.Send_Joint(name="0_"+ball, parent="0", child=ball, type="revolute", position=self.abs_pos[0]+self.size[0]*.5*center2pivot, jointAxis = "1 0 0")
            pyrosim.Send_Cube(name=ball, pos=[0,0,0], size=[0,0,0], colorName="Blue", colorString='    <color rgba="0 0 1.0 1.0"/>')
            pyrosim.Send_Joint(name=ball+"_"+str(j), parent=ball, child=str(j), type="revolute", position=[0,0,0], jointAxis = "0 1 1")
            pyrosim.Send_Cube(name=str(j), pos=self.size[j]*.5*center2pivot, size=self.size[j], colorName=self.GetColor(j)[0], colorString=self.GetColor(j)[1])

        for i in self.bodyPlan:
            if i != 0:
                pivot2center = allDir[self.growDir[i]]
                for j in self.bodyPlan[i]:
                    center2pivot = allDir[self.growDir[j]]
                    pivot2pivot = (center2pivot + pivot2center) * 0.5
                    self.abs_pos[j] = self.abs_pos[i]+center2pivot*.5*(self.size[i]+self.size[j])
                    ball = "m" + str(i) + str(j)
                    pyrosim.Send_Joint(name=str(i)+"_"+ball, parent=str(i), child=ball, type="revolute", position=self.size[i]*pivot2pivot, jointAxis="1 1 0")
                    pyrosim.Send_Cube(name=ball, pos=[0,0,0], size=[0,0,0], colorName="Blue", colorString='    <color rgba="0 0 1.0 1.0"/>')
                    pyrosim.Send_Joint(name=ball+"_"+str(j), parent=ball, child=str(j), type="revolute", position=[0,0,0], jointAxis="0 1 1")
                    pyrosim.Send_Cube(name=str(j), pos=self.size[j]*0.5*center2pivot, size=self.size[j], colorName=self.GetColor(j)[0], colorString=self.GetColor(j)[1])
        pyrosim.End()
        

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        k = 0
        for i in self.bodyPlan:
            if (self.sensorOrNot[numpy.abs(i)]):
                pyrosim.Send_Sensor_Neuron(name = k, linkName = str(i))
                k += 1
        for i in self.bodyPlan:
            for j in self.bodyPlan[i]:
                ball = "m" + str(i) + str(j)
                pyrosim.Send_Motor_Neuron(name = k, jointName = str(i)+"_"+ball)
                k += 1
                pyrosim.Send_Motor_Neuron(name = k, jointName = ball+"_"+str(j))
                k += 1
        for i in range(self.weights.shape[0]):
            for j in range(self.weights.shape[1]):
                pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j + self.numSensorNeurons, weight = self.weights[i][j])
        pyrosim.End()
    
        
    # Initialize the random variables for the robots including
    #  - the length of the limb
    #  - whether each cube has a sensor
    #  - the size of each cube
    # Then it will calculate the the number of sensors and motors, and intialize a
    #  weight matrix based on those numbers.
    def InitializeRandomVariables(self):
        self.length = 2 + numpy.random.randint(2)
        self.sensorOrNot = numpy.random.rand(self.length) < 0.5
        if numpy.sum(self.sensorOrNot) == 0: self.sensorOrNot[0] = True
        self.size = .1 + numpy.random.rand(self.length, 3) * 1.9
        self.numSensorNeurons = 2 * numpy.sum(self.sensorOrNot)
        self.numMotorNeurons = 4 * (self.length - 1)
        self.weights = numpy.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        self.toBotm = self.size[0,2] / 2
    
    def BuildBodyPlan(self):
        self.bodyPlan = {0:[1, -1], 1:[], -1:[]}
        potentialParent = [0, 1]
        for i in range(2, self.length):
          pre_i = numpy.random.choice(potentialParent)
          self.bodyPlan[pre_i].append(i)
          self.bodyPlan[-pre_i].append(-i)
          if len(self.bodyPlan[pre_i]) > 2: potentialParent.remove(pre_i)
          potentialParent.append(i)
          self.bodyPlan[i] = []
          self.bodyPlan[-i] = []
        #print(self.bodyPlan)
    
    def ArrangementPlan(self):
        self.growDir = {}
        remainDir = {_:list(range(6)) for _ in range(-self.length, self.length)}
        for j in self.bodyPlan[0]:
           if j > 0:
             d = numpy.random.choice(remainDir[0])
             remainDir[0].remove(d)
             remainDir[0].remove(5-d)
             remainDir[j].remove(5-d)
             remainDir[-j].remove(d)
             self.growDir[j] = d
             self.growDir[-j] = 5-d
             if d == 3 or d == 2: self.toBotm += self.size[j,2]
             
        for i in self.bodyPlan:
           if i > 0:
               for j in self.bodyPlan[i]:
                 if j > 0:
                     d = numpy.random.choice(remainDir[i])
                     remainDir[i].remove(d)
                     remainDir[-i].remove(5-d)
                     remainDir[j].remove(5-d)
                     remainDir[-j].remove(d)
                     self.growDir[j] = d
                     self.growDir[-j] = 5-d
                     if d == 3 or d == 2: self.toBotm += self.size[j,2]
        #print(self.growDir)
    
    # It takes in the index of the cube
    # It decides the color based on if the cube has a sensor or not
    # It returns the color string and color name of the given cube
    def GetColor(self, idx):
        idx = numpy.abs(idx)
        if self.sensorOrNot[idx]:
            return "Green", '    <color rgba="0 1.0 0 1.0"/>'
        else :
            return "Blue", '    <color rgba="0 0 1.0 1.0"/>'
    
    def MutateBrain(self):
        randomRow = random.randint(0, self.numSensorNeurons - 1)
        randomColumn = random.randint(0, self.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = numpy.random.rand() * 2 - 1
                
    def MutateBody(self):
        n = 2
        idxs = numpy.random.choice(list(range(self.length)), n)
        randSize = .1 + numpy.random.rand(n, 3) * 1.9
        self.size[idxs] = randSize
        
    def SwapSensors(self):
        if True in self.sensorOrNot and False in self.sensorOrNot:
            i_true = numpy.random.choice(numpy.where(self.sensorOrNot==True)[0], 1)
            i_false = numpy.random.choice(numpy.where(self.sensorOrNot==False)[0], 1)
            self.sensorOrNot[i_true] = False
            self.sensorOrNot[i_false] = True
        
    def Set_ID(self, id):
        self.myID = id
        #numpy.random.seed(id)
        
    def save(self, idx):
        filename = "sym" + str(idx) + ".soln"
        config_dict  = {"body":self.bodyPlan, "brain":self.weights, "size":self.size, "sensor":self.sensorOrNot, "abs_pos":self.abs_pos, "grow_dir":self.growDir}
        with open(filename , 'wb') as outp:
            pickle.dump(config_dict, outp, pickle.HIGHEST_PROTOCOL)
    
    def load(self, filename):
        config_dict = pickle.load( open(filename, "rb" ) )
        self.bodyPlan = config_dict["body"]
        self.weights = config_dict["brain"]
        self.size = config_dict["size"]
        self.sensorOrNot = config_dict["sensor"]
        self.abs_pos = config_dict["abs_pos"]
        self.growDir = config_dict["grow_dir"]
        self.Start_Simulation("GUI")
