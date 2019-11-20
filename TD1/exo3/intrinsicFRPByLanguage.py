from utils.instrisicFRP import perform_intrisic_evaluation

import langid


def detect_language(file_name):
    input_file = open(file_name, "r", encoding="utf8")
    language = langid.classify(input_file.read())
    input_file.close()
    return language[0]


def main():
    original_repository_path = "../../Corpus_detourage/Corpus_detourage/html/"
    clean_repository_path = "../../Corpus_detourage/Corpus_detourage/clean/"
    source_repositories_name_and_path = [
            ("JT", "../../Corpus_detourage/Corpus_detourage/clean/JT/"),
            ("BS", "../../Corpus_detourage/Corpus_detourage/clean/BS/"),
            ("JT_langid", "../../Corpus_detourage/Corpus_detourage/clean/JT_langid/"),
            ("JT_trueLg", "../../Corpus_detourage/Corpus_detourage/clean/JT_trueLg/")
        ]
    
    print_header_key = "JT"
    
    perform_intrisic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, detect_language, print_header_key)


if __name__ == '__main__':
    main()
