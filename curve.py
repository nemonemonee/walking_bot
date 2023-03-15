import numpy
import matplotlib.pyplot as plt

controlData = numpy.array(numpy.load("control_curve.npy", allow_pickle=True).tolist())
testData = numpy.array(numpy.load("test_curve.npy", allow_pickle=True).tolist())
symData = numpy.array(numpy.load("sym_curve.npy", allow_pickle=True).tolist())

controlMean = numpy.mean(controlData, axis=0)
testMean = numpy.mean(testData, axis=0)
symMean = numpy.mean(symData, axis=0)

controlMax = controlData[numpy.argmax(controlData[:,-1])]
testMax = testData[numpy.argmax(testData[:,-1])]
symMax = symData[numpy.argmax(symData[:,-1])]

testMean_ = []
symMean_ = []
testMax_ = []
symMax_ = []
for i in range(len(testMean)):
    if i % 3 == 0 :
        testMean_.append(testMean[i])
        testMax_.append(testMax[i])
for i in range(len(symMean)):
    if i % 2 == 0 :
        symMean_.append(testMean[i])
        symMax_.append(testMax[i])

plt.plot(controlMean, label="control")
plt.plot(testMean_, label="coevolution")
plt.plot(symMean_, label="symmetry")

plt.xlabel("Generation")
plt.ylabel("Mean Fitness Score")
plt.legend()
plt.show()


plt.plot(controlMax, label="control")
plt.plot(testMax_, label="coevolution")
plt.plot(symMax_, label="symmetry")

plt.xlabel("Generation")
plt.ylabel("Max Fitness Score")
plt.legend()
plt.show()
