from utils.instrinsicFRP import perform_intrinsic_evaluation

import langid


def detect_language(file_name):
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
            ("JT_trueLg", "../../resources/JT_trueLg/"),
            ("unfluff", "../../resources/unfluff/"),
            ("BTE", "../../resources/BTE/")
        ]
    
    print_header_key = "JT"
    
    perform_intrinsic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, detect_language, print_header_key)


if __name__ == '__main__':
    main()
