"""
This module allows to perform a specific intrinsic evaluation of files by a specified criteria.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

from utils.cleaneval_tool import evaluate_file

import numpy as np
from os import listdir
from os.path import isfile, join


def print_table_format(tools_criterias_data, default_header_key):
    """
    Outputs F-score, Recall and Precision results of the evaluated files.
    """
    print("TOOLS\t\t", end="")
    add_spacing = []
    for criteria in tools_criterias_data[default_header_key]:
        if len(criteria) >= 24:
            print("|" + criteria + "\t", end="")
            if len(criteria) >= 31:
                add_spacing.append(criteria)
        elif len(criteria) >= 16:
            print("|\t" + criteria + "\t", end="")
        elif len(criteria) >= 8:
            print("|\t" + criteria + "\t\t", end="")
        else:
            print("|\t\t" + criteria + "\t\t", end="")
    print()
    print("\t\t", end="")
    for criteria in tools_criterias_data[default_header_key]:
        print("|\tF\tR\tP\t", end="")
        if criteria in add_spacing:
                print("\t", end="")
    print()
    print("----------------", end="")
    for criteria in tools_criterias_data[default_header_key]:
        print("--------------------------------", end="")
        if criteria in add_spacing:
                print("--------", end="")
    print()
    for tool in tools_criterias_data:
        if len(tool) > 7:
            print(tool + "\t", end="")
        else:
            print(tool + "\t\t", end="")
        for criteria in tools_criterias_data[tool]:
            print("|\t" + str(format(tools_criterias_data[tool][criteria]["f-score"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][criteria]["recall"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][criteria]["precision"], ".2f")) + "\t", end="")
            if criteria in add_spacing:
                print("\t", end="")
        print()
    print()


def append_results_to_global_data(results, criterias_data, criteria):
    """
    Allows to append results of a specific file to a global result set
    criterias_data linked to a precise criteria.
    """
    if criteria in criterias_data:
        criterias_data[criteria]["f-score"].append(results["f-score"])
        criterias_data[criteria]["recall"].append(results["recall"])
        criterias_data[criteria]["precision"].append(results["precision"])
    else:
        criterias_data[criteria] = {"f-score": [results["f-score"]], "recall": [results["recall"]], "precision": [results["precision"]]}
    criterias_data["all"]["f-score"].append(results["f-score"])
    criterias_data["all"]["recall"].append(results["recall"])
    criterias_data["all"]["precision"].append(results["precision"])
    return criterias_data


def calculate_mean_values(criterias_data):
    """
    Allows to calculate mean values of the global results criterias_data.
    """
    for criteria in criterias_data:
        criterias_data[criteria]["f-score"] = np.mean(criterias_data[criteria]["f-score"])
        criterias_data[criteria]["recall"] = np.mean(criterias_data[criteria]["recall"])
        criterias_data[criteria]["precision"] = np.mean(criterias_data[criteria]["precision"])
    return criterias_data


def perform_intrinsic_evaluation(original_repository_path, clean_repository_path, source_repositories_name_and_path, criteria_extraction, print_header_key=None):
    """
    Allows to perform an intrinsic evaluation from original files original_repository_path, reference files path
    clean_repository_path, files to evaluate linked to their generator tool source_repositories_name_and_path,
    using an extraction criteria criteria_extraction.
    """
    files_to_evaluate = [f for f in listdir(original_repository_path) if isfile(join(original_repository_path, f))]
    
    global_data = {}
    
    for source_repository_name_and_path in source_repositories_name_and_path:
        criterias_data = {"all": {"f-score": [], "recall": [], "precision": []}}
        for file_name in files_to_evaluate:
            criteria = criteria_extraction(clean_repository_path + file_name)
            results = evaluate_file(source_repository_name_and_path[1] + file_name, clean_repository_path + file_name)
            criterias_data = append_results_to_global_data(results, criterias_data, criteria)
        global_data[source_repository_name_and_path[0]] = calculate_mean_values(criterias_data)
    
    if print_header_key != None:
        print_table_format(global_data, print_header_key)
    
    return global_data
