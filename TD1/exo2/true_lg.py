"""
This module allows to extract text contained in HTML files using JusText composed
with true language identification.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

import justext
import json
import os
from utils.extractor import extract


def jt_truelg_treatement(input_file, output_file, file_name):
    """
    Defines the specific JusText treatment to perform from the input file to the output file.
    It uses true language identification, linked to a specific file, to detect the language to
    use in JusText module.
    """
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
