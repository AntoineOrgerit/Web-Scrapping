*Lisa FOUGERON - François GRÉAU - Antoine ORGERIT

# TD 1 WebScraping

### Notes :

*L'écriture de ce rapport ayant débuté avant la formation du groupe, le code utilisé pour l'exercice 1 diffère de celui pour les autres exercices.*

*Si vous désirez exécuter notre code, pensez à adapter les chemins.*

# Exercice 1 : Utilisation d'outils de détourage

*(L'installation de BoilerPipe 1.2.0.0 ne fonctionnant pas, nous nous sommes rabattu sur la version 1.1)*

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
folder = "D:/DocumentsHDD/M2/WebScraping/Corpus_detourage/" # À ADAPTER SI BESOIN
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

Il ne reste plus qu'à définir des fonctions pour implémenter le fonctionnement des outils. 

## a. JusText

Pour le moment, nous n'identifions pas les langues dans lesquelles sont nos fichiers. L'exécution sera donc probablement plus lente et moins fiable.

```python
import justext

# JusText scraping method
def justextScraping(content):
    return justext.justext(content, "")
```

Résultat : le dossier généré pèse désormais 19,1 Mo.

## b. BoilerPipe

```python
from boilerpipe.extract import Extractor

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
| **Nombre de caractères**                             | 14 659 367 | *x*  | 49 504 518 |
| **Nombre de lignes**                                 | 306 757    | *x*  | 527 095    |
| **Moyenne de la différence du nombre de caractères** | 6 370.41   | *x*  | 26 931.97  |
| **Moyenne de la différence du nombre de lignes**     | 166.6      | *x*  | 296.71     |
| **Écart type du nombre de caractères**               | 5 907.68   | *x*  | 32 151.27  |
| **Écart type du nombre de lignes**                   | 125.18     | *x*  | 214.78     |



### En plus : 

Afin d'observer plus facilement l'efficacité de JusText, nous avons eu l'idée de générer un graphe décrivant la différence du nombre de caractères de chaque fichier entre les résultats de JT et la vérité terrain :

![difference_clean_jt](./resources/difference_clean_jt.png)

Nous pouvons alors facilement observer que mis à part de rares extrêmes, les différences sont relativement faibles.

# Exercice 2 : Guider le scraping avec la reconnaissance de langue

Afin d'accélérer l'exécution de JusText, on veut connaître la langue de chaque fichier afin de l'indiquer lors du scraping. Pour ce faire, deux choix s'offrent à nous. On peut utiliser la librairie ***langid.py*** :

```python
def jt_langid_treatement(input_file, output_file):
    if input_file.read() != " ":
        input_file.seek(0)
        language = langid.classify(input_file.read())
        language = languages.get(alpha2=language[0]).name
        
        # Greek is the only badly formatted one so we convert "Modern Greek (1453-)" into "Greek"
        if "Greek" in language:
            language = "Greek"
        # If language is unspecified, we choose English
        if language not in justext.get_stoplists():
            language = "English"
        
        input_file.seek(0)
        paragraphs = justext.justext(input_file.read(), justext.get_stoplist(language))
        
        for paragraph in paragraphs:
            output_file.write("<p>" + paragraph.text.replace("\n", " ") + "</p>\n")
    else:
        output_file.write(" ")
```

...ou bien le fichier JSON qui nous est fourni :

```python
def jt_truelg_treatement(input_file, output_file, file_name):
    if input_file.read() != " ":
        input_file.seek(0)
        languages = json.load(open("../../../resources/doc_lg.json"))
        
        language = languages[os.path.basename(file_name)]
        
        # If language is unspecified, we choose English 
        if language not in justext.get_stoplists():
            language = "English"
        
        paragraphs = justext.justext(input_file.read(), justext.get_stoplist(language))
        
        for paragraph in paragraphs:
            output_file.write("<p>" + paragraph.text.replace("\n", " ") + "</p>\n")
    else:
        output_file.write(" ")
```

En recalculant les métriques précédentes pour JusText, on obtient les valeurs suivantes :

| Métrique                                             | Valeur pour JT_langid |
| ---------------------------------------------------- | --------------------- |
| **Nombre de caractères**                             | 14 048 036            |
| **Nombre de ligne**                                  | 306 755               |
| **Moyenne de la différence du nombre de caractères** | 6 011.14              |
| **Moyenne de la différence du nombre de lignes**     | 166.79                |
| **Écart type du nombre de caractères**               | 5 702.18              |
| **Écart type du nombre de lignes**                   | 125.18                |

On se rend compte que les valeurs sont similaires à celles obtenues sans préciser la langue. Nous supposons que la différence se fait plutôt dans la vitesse d'exécution.

___

*PROPOSITION : RELEVER LES TEMPS AVEC ET SANS LA LANGUE PRÉCISÉE*

| Langue        | Temps d'exécution en ms |
| ------------- | ----------------------- |
| Non spécifiée |                         |
| Spécifiée     |                         |

___

# Exercice 3 : Évaluation intrinsèque

* ## Mesures  des valeurs de la F-Mesures, du Rappel et de la Précision  en fonction des langues

<table>
  <tr>
    <th rowspan="2" align="center" style="vertical-align:middle">OUTILS<br></th>
    <th colspan="3" align="center">All</th>
    <th colspan="3" align="center">el</th>
  </tr>
  <tr>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
  </tr>
  <tr>
    <td align="center">JT</td>
    <td align="center">34.67</td>
    <td align="center">88.81</td>
    <td align="center">23.90</td>
    <td align="center">44.36</td>
    <td align="center">97.58</td>
    <td align="center">30.45</td>
  </tr>
  <tr>
    <td align="center">BS</td>
    <td align="center">21.14</td>
    <td align="center">88.44</td>
    <td align="center">13.32</td>
    <td align="center">23.43</td>
    <td align="center">97.49</td>
    <td align="center">14.83</td>
  </tr>
  <tr>
    <td align="center">JT_langid</td>
    <td align="center">38.91</td>
    <td align="center">92.89</td>
    <td align="center">27.38</td>
    <td align="center">48.14</td>
    <td align="center">96.61</td>
    <td align="center">34.04</td>
  </tr>
  <tr>
    <td align="center">JT_trueLg</td>
    <td align="center">38.91</td>
    <td align="center">92.89</td>
    <td align="center">27.38</td>
    <td align="center">48.14</td>
    <td align="center">96.61</td>
    <td align="center">34.04</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" align="center" style="vertical-align:middle">OUTILS<br></th>
    <th colspan="3" align="center">pl</th>
    <th colspan="3" align="center">ru</th>
  </tr>
  <tr>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
  </tr>
  <tr>
    <td align="center">JT</td>
    <td align="center">43.08</td>
    <td align="center">94.29</td>
    <td align="center">30.34</td>
    <td align="center">31.19</td>
    <td align="center">93.81</td>
    <td align="center">21.14</td>
  </tr>
  <tr>
    <td align="center">BS</td>
    <td align="center">30.37</td>
    <td align="center">94.20</td>
    <td align="center">19.48</td>
    <td align="center">18.06</td>
    <td align="center">94.04</td>
    <td align="center">10.92</td>
  </tr>
  <tr>
    <td align="center">JT_langid</td>
    <td align="center">46.11</td>
    <td align="center">93.10</td>
    <td align="center">33.26</td>
    <td align="center">32.80</td>
    <td align="center">89.94</td>
    <td align="center">22.58</td>
  </tr>
  <tr>
    <td align="center">JT_trueLg</td>
    <td align="center">46.11</td>
    <td align="center">93.10</td>
    <td align="center">33.26</td>
    <td align="center">32.80</td>
    <td align="center">89.94</td>
    <td align="center">22.58</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" align="center" style="vertical-align:middle">OUTILS<br></th>
    <th colspan="3" align="center">en</th>
    <th colspan="3" align="center">zh</th>
  </tr>
  <tr>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
  </tr>
  <tr>
    <td align="center">JT</td>
    <td align="center">44.59</td>
    <td align="center">96.41</td>
    <td align="center">31.25</td>
    <td align="center">13.09</td>
    <td align="center">66.96</td>
    <td align="center">8.30</td>
  </tr>
  <tr>
    <td align="center">BS</td>
    <td align="center">30.40</td>
    <td align="center">96.02</td>
    <td align="center">19.37</td>
    <td align="center">4.50</td>
    <td align="center">65.85</td>
    <td align="center">2.59</td>
  </tr>
  <tr>
    <td align="center">JT_langid</td>
    <td align="center">49.51</td>
    <td align="center">98.04</td>
    <td align="center">35.63</td>
    <td align="center">19.35</td>
    <td align="center">86.13</td>
    <td align="center">12.39</td>
  </tr>
  <tr>
    <td align="center">JT_trueLg</td>
    <td align="center">49.51</td>
    <td align="center">98.04</td>
    <td align="center">35.63</td>
    <td align="center">19.35</td>
    <td align="center">86.13</td>
    <td align="center">12.39</td>
  </tr>
</table>



* ## Mesures  des valeurs de la F-Mesure, du Rappel et de la Précision  en fonction des sources

<table>
  <tr>
    <th rowspan="2" align="center" style="vertical-align:middle">OUTILS<br></th>
    <th colspan="3" align="center">All</th>
    <th colspan="3" align="center">www.express.gr</th>
  </tr>
  <tr>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
  </tr>
  <tr>
    <td align="center">JT</td>
    <td align="center">34.67</td>
    <td align="center">88.81</td>
    <td align="center">23.90</td>
    <td align="center">53.00</td>
    <td align="center">97.64</td>
    <td align="center">37.06</td>
  </tr>
  <tr>
    <td align="center">BS</td>
    <td align="center">21.14</td>
    <td align="center">88.44</td>
    <td align="center">13.32</td>
    <td align="center">5.40</td>
    <td align="center">97.73</td>
    <td align="center">2.79</td>
  </tr>
  <tr>
    <td align="center">JT_langid</td>
    <td align="center">38.91</td>
    <td align="center">92.89</td>
    <td align="center">27.38</td>
    <td align="center">57.64</td>
    <td align="center">97.45</td>
    <td align="center">41.67</td>
  </tr>
  <tr>
    <td align="center">JT_trueLg</td>
    <td align="center">38.91</td>
    <td align="center">92.89</td>
    <td align="center">27.38</td>
    <td align="center">57.64</td>
    <td align="center">97.45</td>
    <td align="center">41.67</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" align="center" style="vertical-align:middle">OUTILS<br></th>
    <th colspan="3" align="center">goodcontents.net</th>
    <th colspan="3" align="center">biolog.pl</th>
  </tr>
  <tr>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
    <td align="center">F</td>
    <td align="center">R</td>
    <td align="center">P</td>
  </tr>
  <tr>
    <td align="center">JT</td>
    <td align="center">54.86</td>
    <td align="center">97.67</td>
    <td align="center">38.75</td>
    <td align="center">63.92</td>
    <td align="center">98.10</td>
    <td align="center">48.56</td>
  </tr>
  <tr>
    <td align="center">BS</td>
    <td align="center">49.65</td>
    <td align="center">99.13</td>
    <td align="center">33.54</td>
    <td align="center">42.77</td>
    <td align="center">98.21</td>
    <td align="center">28.19</td>
  </tr>
  <tr>
    <td align="center">JT_langid</td>
    <td align="center">57.63</td>
    <td align="center">96.18</td>
    <td align="center">41.75</td>
    <td align="center">65.97</td>
    <td align="center">97.33</td>
    <td align="center">51.06</td>
  </tr>
  <tr>
    <td align="center">JT_trueLg</td>
    <td align="center">57.63</td>
    <td align="center">96.18</td>
    <td align="center">41.75</td>
    <td align="center">65.97</td>
    <td align="center">97.33</td>
    <td align="center">51.06</td>
  </tr>
</table>

