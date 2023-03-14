import numpy

fitData = numpy.load("fitData.npy", allow_pickle=True).tolist()
import matplotlib.pyplot as plt
for i in range(len(fitData)):
    plt.plot(fitData[i])
plt.xlabel("Generation")
plt.ylabel("Fitness Score")
plt.show()
