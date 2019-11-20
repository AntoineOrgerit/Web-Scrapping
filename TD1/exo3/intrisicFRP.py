from exo3.cleaneval_tool import evaluate_file

import numpy as np
import langid
from os import listdir
from os.path import isfile, join


def print_language_results(language_results):
    for language in language_results:
        print("Language '" + language + "':")
        # print("\tF-score: " + str(np.mean(language_results[language]["f-score"])))
        # print("\tRecall: " + str(np.mean(language_results[language]["recall"])))
        # print("\tRPrecision: " + str(np.mean(language_results[language]["precision"])))


def detect_language(file_name):
    input_file = open(file_name, "r", encoding="utf8")
    language = langid.classify(input_file.read())
    input_file.close()
    return language[0]


def append_results_to_language_data(results, language_data, language):
    if language in language_data:
        language_data[language]["f-score"].append(results["f-score"])
        language_data[language]["recall"].append(results["recall"])
        language_data[language]["precision"].append(results["precision"])
    else:
        language_data[language] = {"f-score": [results["f-score"]], "recall": [results["recall"]], "precision": [results["precision"]]}
    language_data["all"]["f-score"].append(results["f-score"])
    language_data["all"]["recall"].append(results["recall"])
    language_data["all"]["precision"].append(results["precision"])
    return language_data


def calculate_mean_values(language_data):
    for language in language_data:
        language_data[language]["f-score"] = np.mean(language_data[language]["f-score"])
        language_data[language]["recall"] = np.mean(language_data[language]["recall"])
        language_data[language]["precision"] = np.mean(language_data[language]["precision"])
    return language_data


def perform_intrisic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path):
    files_to_evaluate = [f for f in listdir(original_repository_path) if isfile(join(original_repository_path, f))]
    
    tools_language_data = {}
    
    for source_repository_name_and_path in source_repositories_name_and_path:
        language_data = {"all": {"f-score": [], "recall": [], "precision": []}}
        for file_name in files_to_evaluate:
            language = detect_language(clean_repository_path + file_name)
            results = evaluate_file(source_repository_name_and_path[1] + file_name, clean_repository_path + file_name)
            language_data = append_results_to_language_data(results, language_data, language)
        tools_language_data[source_repository_name_and_path[0]] = calculate_mean_values(language_data)
    
    return tools_language_data


def print_table_format(tools_language_data, default_header_key):
    print("OUTILS\t\t", end="")
    for language in tools_language_data[default_header_key]:
        print("|\t\t\t\t" + language + "\t\t\t\t\t", end="")
    print()
    print("\t\t", end="")
    for language in tools_language_data[default_header_key]:
        print("|\tF\t\t\tR\t\t\tP\t\t", end="")
    print()
    for language in tools_language_data[default_header_key]:
        print("------------------------------------------------------", end="")
    print()
    for tool in tools_language_data:
        if len(tool) > 7:
            print(tool + "\t", end="")
        else:
            print(tool + "\t\t", end="")
        for language in tools_language_data[tool]:
            print("|" + str(tools_language_data[tool][language]["f-score"]) + "\t" + str(tools_language_data[tool][language]["recall"]) + "\t" + str(tools_language_data[tool][language]["precision"]) + "\t", end="")
        print()


def main():
    original_repository_path = "../../Corpus_detourage/Corpus_detourage/html/"
    clean_repository_path = "../../Corpus_detourage/Corpus_detourage/clean/"
    source_repositories_name_and_path = [
            ("JT", "../../Corpus_detourage/Corpus_detourage/clean/JT/"),
            ("BS", "../../Corpus_detourage/Corpus_detourage/clean/BS/"),
            ("JT_langid", "../../Corpus_detourage/Corpus_detourage/clean/JT_langid/"),
            ("JT_trueLg", "../../Corpus_detourage/Corpus_detourage/clean/JT_trueLg/")
        ]
    
    tools_language_data = perform_intrisic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path)
    print_table_format(tools_language_data, "JT")


if __name__ == '__main__':
    main()
