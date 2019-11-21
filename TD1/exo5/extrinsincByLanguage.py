from utils.extrinsic import perform_extrinsic_evaluation

import langid


def detect_language(file_name):
    input_file = open(file_name, "r", encoding="utf8")
    language = langid.classify(input_file.read())
    input_file.close()
    return language[0]


def main():
    clean_repository_path_and_json = ("../../../resources/clean/", "../../../resources/daniel.json")
    source_repositories_name_and_path = [
            ("JT", "../../../resources/JT/"),
            ("BS", "../../../resources/BS/"),
            ("JT_langid", "../../../resources/JT_langid/"),
            ("JT_trueLg", "../../../resources/JT_trueLg/"),
            ("unfluff", "../../../resources/unfluff/"),
            ("BTE", "../../../resources/BTE/")
        ]
    source_repositories_name_and_path = [
            ("JT", "../../../resources/JT/"),
            ("unfluff", "../../../resources/unfluff/")
        ]
    
    print_header_key = "JT"
    
    perform_extrinsic_evaluation(clean_repository_path_and_json, source_repositories_name_and_path, detect_language, print_header_key)


if __name__ == '__main__':
    main()
