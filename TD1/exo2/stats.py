from utils.stats import generate_global_statistics

def main():
    cleaned_repository_path = "../../Corpus_detourage/Corpus_detourage/clean/"
    source_repositories_name_and_path = [
            ("JT", "../../Corpus_detourage/Corpus_detourage/clean/JT/"),
            ("BS", "../../Corpus_detourage/Corpus_detourage/clean/BS/"),
            ("JT_langid", "../../Corpus_detourage/Corpus_detourage/clean/JT_langid/"),
            ("JT_trueLg", "../../Corpus_detourage/Corpus_detourage/clean/JT_trueLg/")
        ]
    source_files_repository = "../../Corpus_detourage/Corpus_detourage/html/"
    generate_global_statistics(source_repositories_name_and_path, cleaned_repository_path, source_files_repository)

if __name__ == '__main__':
    main()
