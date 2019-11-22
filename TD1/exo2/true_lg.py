import justext
import json
import os
from utils.extractor import extract

def jt_truelg_treatement(input_file, output_file, file_name):
    if input_file.read() != " ":
        input_file.seek(0)
        languages = json.load(open("../../resources/doc_lg.json"))
        
        language = languages[os.path.basename(file_name)]
        if language not in justext.get_stoplists():
            language = "English"
        
        paragraphs = justext.justext(input_file.read(), justext.get_stoplist(language))
        
        for paragraph in paragraphs:
            output_file.write("<p>" + paragraph.text.replace("\n", " ") + "</p>\n")
    else:
        output_file.write(" ")


def main():
    extract("../../resources/JT/", "../../resources/JT_trueLg/", jt_truelg_treatement)

if __name__ == '__main__':
    main()
