import justext
import langid
from iso639 import languages
from utils.extractor import extract

def jt_langid_treatement(input_file, output_file):
    language = langid.classify(input_file.read())
    language = languages.get(alpha2=language[0]).name
    if "Greek" in language:
        language = "Greek"
    if language not in justext.get_stoplists():
        language = "English"
    
    input_file.seek(0)
    paragraphs = justext.justext(input_file.read(), justext.get_stoplist(language))
    
    for paragraph in paragraphs:
        output_file.write("<p>" + paragraph.text.replace("\n", " ") + "</p>\n")


def main():
    extract("../../Corpus_detourage/Corpus_detourage/clean/JT/", "../../Corpus_detourage/Corpus_detourage/clean/JT_langid/", jt_langid_treatement)

if __name__ == '__main__':
    main()
