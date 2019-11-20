from boilerpipe.extract import Extractor
from os import listdir
from os.path import isfile, join

filesToExtractContentFrom = [f for f in listdir("../Corpus_detourage/Corpus_detourage/html/") if isfile(join("../Corpus_detourage/Corpus_detourage/html/", f))]

for fileToExtractContentFrom in filesToExtractContentFrom:
    
    inputFile = open("../Corpus_detourage/Corpus_detourage/html/" + fileToExtractContentFrom, "r", encoding="utf8", errors="replace")
    outputFile = open("../Corpus_detourage/Corpus_detourage/clean/BP/" + fileToExtractContentFrom, "w", encoding="utf8", errors="replace")
    
    extractor = Extractor(extractor='ArticleExtractor', url="../Corpus_detourage/Corpus_detourage/html/" + fileToExtractContentFrom)
    outputFile.write(extractor.getHTML())
    
    outputFile.close()
    inputFile.close()
