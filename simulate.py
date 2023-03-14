import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()

#numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
#numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)
