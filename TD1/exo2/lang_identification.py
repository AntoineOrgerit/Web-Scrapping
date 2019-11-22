"""
This module allows to extract text contained in HTML files using JusText composed
with langid language identification.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

import justext
import langid
from iso639 import languages
from utils.extractor import extract


def jt_langid_treatement(input_file, output_file):
    """
    Defines the specific JusText treatment to perform from the input file to the output file.
    It uses the langid module to detect the language to use in JusText module.
    """
    if input_file.read() != " ":
        input_file.seek(0)
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
    else:
        output_file.write(" ")


def main():
    extract("../../resources/JT/", "../../resources/JT_langid/", jt_langid_treatement)


if __name__ == '__main__':
    main()
