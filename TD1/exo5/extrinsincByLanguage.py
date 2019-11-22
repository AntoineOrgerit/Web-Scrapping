"""
This module allows to perform an extrinsic evaluation by language of different generated files by JusText, BoilerPipe,
BeautifulSoup, langid and true language identification, unfluff and BTE.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

from utils.extrinsic import perform_extrinsic_evaluation


def extract_language(infos):
    """
    Allows to extract the language used in a document from its JSON entity informations.
    """
    return infos["language"]


def main():
    clean_repository_path_and_json = ("../../resources/clean/", "../../resources/daniel.json")
    source_repositories_name_and_path = [
            ("JT", "../../resources/JT/"),
            ("BP", "../../resources/BP/"),
            ("BS", "../../resources/BS/"),
            ("JT_langid", "../../resources/JT_langid/"),
            ("JT_trueLg", "../../resources/JT_trueLg/"),
            ("unfluff", "../../resources/unfluff/"),
            ("BTE", "../../resources/BTE/")
        ]
    
    print_header_key = "JT"
    
    perform_extrinsic_evaluation(clean_repository_path_and_json, source_repositories_name_and_path, extract_language, print_header_key)


if __name__ == '__main__':
    main()
