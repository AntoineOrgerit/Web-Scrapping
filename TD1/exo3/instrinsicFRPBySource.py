from utils.instrisicFRP import perform_intrisic_evaluation


def extract_source(file_name):
    splited = file_name.split("/")
    return splited[len(splited) - 1].split("_")[1]


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
    
    perform_intrisic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, extract_source, print_header_key)


if __name__ == '__main__':
    main()
