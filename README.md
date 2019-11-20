François GRÉAU													TD 1 WebScraping
Lisa FOUGERON
Antoine ORGERIT

_________

# Exercice 1 : Utilisation d'outils de détourage

*(L'installation de BoilerPipe 1.2.0.0 ne fonctionnant pas, je me suis rabattu sur la version 1.1)*

Dossier ***html*** :

* 127 002 561 caractères et 2 345 719 lignes

* 129 Mo.

```python
import glob
import os

# Parses through the given paths and applies the given scraping method
def parseFile(inputPath, outputPath, fileName, scrapingFunction):
    page = open(inputPath + fileName, encoding="utf-8", errors="ignore")
    pageContent = page.read()
    page.close()
    
    # Exits if the file is empty
    if pageContent == "":
        return
    
    output = open(outputPath + fileName, "a", encoding="utf-8", errors="ignore")
    paragraphs = scrapingFunction(pageContent)
    for paragraph in paragraphs:
        output.write("<p> " + paragraph.text + " </p>\n")
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

Résultat : le dossier généré pèse désormais x Mo.

## c. BeautifulSoup

```python

```

Résultat : le dossier généré pèse désormais x Mo.

## Comparaisons :

Afin de calculer les moyennes des différences du nombre de caractères et de lignes entre les résultats et les 

|                                                  | JT         | BP   | BS   |
| ------------------------------------------------ | ---------- | ---- | ---- |
| nombre de caractères                             | 14 659 366 | x    |      |
| nombre de lignes                                 | 339 163    | x    |      |
| Moyenne de la différence du nombre de caractères | 6 357.23   | x    |      |
| Moyenne de la différence du nombre de lignes     | 186.73     | x    |      |
| Écart type du nombre de caractères               | 8 688.09   | x    |      |
| Écart type du nombre de lignes                   | 242.79     | x    |      |



