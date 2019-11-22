"""
This module allows to perform an intrinsic evaluation by source of different generated files by JusText, BoilerPipe,
BeautifulSoup, langid and true language identification.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

from utils.instrinsicFRP import perform_intrinsic_evaluation


def extract_source(file_name):
    """
    Allows to detect the source contained in the file name of a document.
    """
    splited = file_name.split("/")
    return splited[len(splited) - 1].split("_")[1]


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
    
    perform_intrinsic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, extract_source, print_header_key)


if __name__ == '__main__':
    main()
