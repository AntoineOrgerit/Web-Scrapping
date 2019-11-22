from utils.extrinsic import perform_extrinsic_evaluation


def extract_language(infos):
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
