from solution import SOLUTION
import constants as c
import copy
import os
import numpy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm body*.urdf")
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.nextAvailableID = 0
        self.parents = dict()
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.fitnessRecords = numpy.zeros((c.populationSize, c.numberOfGenerations))
        

    def Evolve(self):
        self.Evaluate(self.parents)
        for self.currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            if (self.currentGeneration + 1) % 100 == 0:
                for p in self.parents:
                    self.parents[p].save()
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()
    
    def Spawn(self):
        self.children = dict()
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].MutateBody()
            self.children[i].SwapSensors()
            self.children[i].MutateBrain()
#            if self.currentGeneration % 3 == 1:
#                self.children[i].MutateBody()
#            elif self.currentGeneration % 3 == 2:
#                self.children[i].SwapSensors()
#            else:
#                self.children[i].MutateBrain()
        
    def Select(self):
        for i in self.parents:
            print(self.parents[i].fitness, self.children[i].fitness)
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = copy.deepcopy(self.children[i])
            self.fitnessRecords[i, self.currentGeneration] = self.parents[i].fitness
        print("Generation#{}".format(self.currentGeneration))
       
    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()
        
        
        
    def Show_Best(self):
        t = 0
        input()
        print(self.fitnessRecords)
        numpy.save("fitData.npy", self.fitnessRecords)
        top5 = numpy.zeros(5)
        for i in self.parents:
            self.parents[i].Start_Simulation("GUI")


