"""
This module allows to perform an intrinsic evaluation by language of different generated files by JusText, BoilerPipe,
BeautifulSoup, langid and true language identification.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

from utils.instrinsicFRP import perform_intrinsic_evaluation

import langid


def detect_language(file_name):
    """
    Allows to detect the language used in a document.
    It uses the langid module to detect the language.
    """
    input_file = open(file_name, "r", encoding="utf8")
    language = langid.classify(input_file.read())
    input_file.close()
    return language[0]


def main():
    original_repository_path = "../../resources/html/"
    clean_repository_path = "../../resources/clean/"
    source_repositories_name_and_path = [
            ("JT", "../../resources/JT/"),
            ("BP", "../../resources/BP/"),
            ("BS", "../../resources/BS/"),
            ("JT_langid", "../../resources/JT_langid/"),
            ("JT_trueLg", "../../resources/JT_trueLg/")
        ]
    
    print_header_key = "JT"
    
    perform_intrinsic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, detect_language, print_header_key)


if __name__ == '__main__':
    main()
