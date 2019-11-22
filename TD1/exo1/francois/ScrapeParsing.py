import justext
import glob
#from boilerpipe.extract import Extractor
import os
from bs4 import BeautifulSoup

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

# JusText scraping method
def justextScraping(content):
    return justext.justext(content, "")

# BoilerPipe scraping method
def boilerPipeScraping(content):
    #extractor = Extractor(extractor="ArticleExtractor", url="file:" + content)
    #return extractor.getText
    return

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

# Parent folder and list of files
folder = "../../../resources/"
files = [f for f in glob.glob(folder + "html/*")]

index = 1
for file in files: 
    os.system("cls")
    parseFile(folder + "html/", folder + "output/", file.split('\\')[-1], justextScraping)
    print("parsed " + str(index) + " out of " + str(len(files)) + " files")
    index += 1