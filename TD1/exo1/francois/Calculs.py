import os
import math

def calculateAverage(referenceFolder, targetFolder):
    path = "D:/DocumentsHDD/M2/WebScraping/Corpus_detourage/"

    nbFiles = len(os.listdir(path + referenceFolder))

    initialCharNumber = 0
    initialLineNumber = 0
    folderCharNumber = 0
    folderLineNumber = 0
    varianceChar = 0
    varianceLine = 0

    for fileName in os.listdir(path + referenceFolder):

        # Reference folder
        currentFile = open(path + referenceFolder + "/" + fileName, encoding="utf-8", errors="ignore")
        content = currentFile.read()
        currentFile.close()
        initialCharNumber += len(content)
        initialLineNumber += content.count('\n')

        # Target folder
        currentFileTarget = open(path + targetFolder + "/" + fileName, encoding="utf-8", errors="ignore")
        contentTarget = currentFileTarget.read()
        currentFileTarget.close()
        folderCharNumber += len(contentTarget)
        folderLineNumber += contentTarget.count('\n')

        varianceChar += pow(len(content) - len(contentTarget), 2)
        varianceLine += pow(content.count('\n') - contentTarget.count('\n'), 2) 

    print("\nb total de caractères du dossier " + referenceFolder + " : " + str(initialCharNumber))
    print("nb total de lignes du dossier " + referenceFolder + " : " + str(initialLineNumber))
    
    print("\nnb total de caractères du dossier " + targetFolder + " : " + str(folderCharNumber))
    print("nb total de lignes du dossier " + targetFolder + " : " + str(folderLineNumber))

    print("\ndifférence moyenne de caractères : " + str((initialCharNumber - folderCharNumber) / nbFiles) )
    print("différence moyenne de lignes : " + str((initialLineNumber - folderLineNumber) / nbFiles) )

    print("\nvariance caractères : " + str(varianceChar / nbFiles) + " -> Ecart type caractères : " + str(math.sqrt(varianceChar / nbFiles)))
    print("variance lignes : " + str(varianceLine / nbFiles) + " -> Ecart type lignes : " + str(math.sqrt(varianceLine / nbFiles)))

# Attention ! Ne pas itérer à partir des fichiers de "clean" car il y a des fichiers en trop
calculateAverage("JT", "clean")