import os
import matplotlib.pyplot as plt

path = "../../../resources/"
targetFolder = "JT"

pointsCleanChar = []
pointsCompChar = []

pointsCleanLine = []
pointsCompLine = []

differenceChar = []

for fileName in os.listdir(path + targetFolder):
    cleanFile = open(path + "clean/" + fileName, encoding="utf-8", errors="ignore")
    cleanContent = cleanFile.read()
    cleanFile.close()
    
    targetFile = open(path + targetFolder + "/" + fileName, encoding="utf-8", errors="ignore")
    targetContent = targetFile.read()
    targetFile.close()

    pointsCleanChar.append(len(cleanContent))
    pointsCompChar.append(len(targetContent))

    differenceChar.append(len(targetContent) - len(cleanContent))

print(len(pointsCleanChar))
print(len(pointsCompChar))

axisX = [0] * len(pointsCompChar)
#plt.plot(index, pointsCleanChar, color='g')
#plt.plot(index, pointsCompChar)
plt.plot( sorted(differenceChar))
plt.plot( axisX, color="black")
plt.show()

