import pyrosim.pyrosim as pyrosim
import numpy

def Create_World():
  pyrosim.Start_SDF("world.sdf")
  pyrosim.Send_Cube(name="Box", pos=[-1,-1,0.5] , size=[1,1,1])
  pyrosim.End()

def Create_Robot():
  Generate_Body()
  Generate_Brain()
 
def Generate_Body():
  pyrosim.Start_URDF("body.urdf")
  size_0 = 0.5 + 2 * numpy.random.rand(3)
  pyrosim.Send_Cube(name="0", pos=[0,0,0.5], size=size_0)
  offset = size_0[1] / 2
  pyrosim.Send_Joint(name = "0_1", parent= "0", child = "1", type = "revolute", position = [0,offset,0.5], jointAxis = "1 0 0")
  size_1 = 0.5 + 2 * numpy.random.rand(3)
  pyrosim.Send_Cube(name="1", pos=[0,offset,0] , size=size_1)
  offset = size_1[1] / 2
  for i in range(2, length):
    size_i = 0.5 + 2 * numpy.random.rand(3)
    pyrosim.Send_Joint(name = str(i-1)+"_"+str(i) , parent= str(i-1) , child = str(i) , type = "revolute", position = [0,offset,0.5], jointAxis = "1 0 0")
    offset = size_i[1] / 2
    pyrosim.Send_Cube(name=str(i), pos=[0,offset,0] , size=size_i)
  pyrosim.End()
  
def Generate_Brain():
  pyrosim.Start_NeuralNetwork("brain0.nndf")
  j = 0
  for i in range(length):
    if (sensorOrNot[i]):
      pyrosim.Send_Sensor_Neuron(name = j, linkName = str(i))
      j += 1
  for i in range(1, length):
    pyrosim.Send_Motor_Neuron(name = j, jointName = str(i-1)+"_"+str(i))
    j += 1
  for i in range(numSensorNeurons):
    for j in range(numMotorNeurons):
      pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j + numSensorNeurons, weight = weights[i][j])
  pyrosim.End()

length = numpy.random.randint(10) + 1
sensorOrNot = numpy.random.rand(length) < 0.5
numSensorNeurons = numpy.sum(sensorOrNot)
numMotorNeurons = length
weights = numpy.random.rand(numSensorNeurons,numMotorNeurons) * 2 - 1
        
Create_World()
Create_Robot()
