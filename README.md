Lisa FOUGERON - François GRÉAU - Antoine ORGERIT

# TD 1 WebScraping

_________

# Exercice 1 : Utilisation d'outils de détourage

_____

*(L'installation de BoilerPipe 1.2.0.0 ne fonctionnant pas, je me suis rabattu sur la version 1.1)*

Nous nous basons sur le dossier ***html*** fourni, possédant les caractéristiques suivantes :

* 1694 fichiers, totalisant 127 002 561 caractères en 2 345 719 lignes
* 129 Mo.

On veut utiliser trois outils afin d'extraire le contenu des articles de ces fichiers. Pour ce faire, Nous avons développé un code en Python permettant de créer des fichiers contenant les résultats en spécifiant une méthode de scraping :

```python
import glob
import os

# Parses through the given paths and applies the given scraping method
def parseFile(inputPath, outputPath, fileName, scrapingFunction):
    page = open(inputPath + fileName, encoding="utf-8", errors="ignore")
    pageContent = page.read()
    page.close()

    output = open(outputPath + fileName, "a", encoding="utf-8", errors="ignore")

    # Creates an empty file if the original file is empty
    if pageContent == "":
        output.write(" ")
    else:
        paragraphs = scrapingFunction(pageContent)
        for paragraph in paragraphs:
            if (paragraph.text):
                output.write("<p> " + paragraph.text.replace('\n', ' ') + " </p>\n")
        output.close()

# Parent folder and list of files
folder = "D:/DocumentsHDD/M2/WebScraping/Corpus_detourage/"
files = [f for f in glob.glob(folder + "html/*")]

# Placeholder for the future scraping methods
def scrapingMethodPlaceholder()

index = 1
for file in files: 
    os.system("cls")
    parseFile(folder + "html/", folder + "output/", file.split('\\')[-1], scrapingMethodPlaceholder)
    print("parsed " + str(index) + " out of " + str(len(files)) + " files")
    index += 1
```

Il ne reste plus qu'à définir des fonctions pour implémenter le fonctionnement des outils

## a. JusText

```python
import justext

# JusText scraping method
def justextScraping(content):
    return justext.justext(content, "")
```

Résultat : le dossier généré pèse désormais 19,1 Mo.

## b. BoilerPipe

```python
# BoilerPipe scraping method
def boilerPipeScraping(content):
    extractor = Extractor(extractor="ArticleExtractor", url="file:" + content)
    return extractor.getText
```

*Ceci est le code théorique pour BoilerPipe. Malheureusement, après de nombreuses tentatives infructueuses pour faire fonctionner la librairie, nous avons décidé de le laisser de coté.*

## c. BeautifulSoup

```python
from bs4 import BeautifulSoup

# Since the parseFile method requires objects with a text attribute
class Struct:
  def __init__(self, **entries):
    self.__dict__.update(entries)

# BeautifulSoup scraping method
def beautifulSoupScraping(content):
    soup = BeautifulSoup(content).stripped_strings
    out = []
    for elem in soup:
        out.append( Struct( **{"text": elem} ) )
    return out
```

Résultat : le dossier généré pèse désormais 53,5 Mo.

## Comparaisons :

Afin de calculer les métriques relatives au nombre de caractères et de lignes entre les résultats obtenus et la référence, nous avons écrit le script suivant en python :

```python
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
```

Grace à cela, nous relevons les données suivantes :

|                                                      | JT         | BP   | BS         |
| ---------------------------------------------------- | ---------- | ---- | ---------- |
| **nombre de caractères**                             | 14 659 366 | *x*  | 49 504 518 |
| **nombre de lignes**                                 | 305 062    | *x*  | 525 400    |
| **Moyenne de la différence du nombre de caractères** | 6 357.23   | *x*  | 26 926.98  |
| **Moyenne de la différence du nombre de lignes**     | 166.6      | *x*  | 296.67     |
| **Écart type du nombre de caractères**               | 8 688.09   | *x*  | 41 940.85  |
| **Écart type du nombre de lignes**                   | 208.54     | *x*  | 366.29     |



### En plus : 

Afin d'observer plus facilement l'efficacité de JusText, nous avons eu l'idée de générer un graphe décrivant la différence du nombre de caractères de chaque fichier entre les résultats de JT et la vérité terrain :

![difference_clean_jt](.\resources\difference_clean_jt.png)

Nous pouvons alors facilement observer que pour de rares extrêmes, les différences sont relativement faibles.



# Exercice 2 : Guider le scraping avec la reconnaissance de langue

_____

