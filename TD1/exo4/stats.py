from utils.stats import generate_global_statistics

def main():
    cleaned_repository_path = "../../../resources/clean/"
    source_repositories_name_and_path = [
            ("JT", "../../../resources/JT/"),
            ("BS", "../../../resources/BS/"),
            ("JT_langid", "../../../resources/JT_langid/"),
            ("JT_trueLg", "../../../resources/JT_trueLg/"),
            ("unfluff", "../../../resources/unfluff/"),
            ("BTE", "../../../resources/BTE/")
        ]
    source_files_repository = "../../../resources/html/"
    generate_global_statistics(source_repositories_name_and_path, cleaned_repository_path, source_files_repository)

if __name__ == '__main__':
    main()
