"""
This module allows to perform statistics of files compared to an aimed set of files.

Antoine Orgerit - François Gréau - Lisa Fougeron
La Rochelle Université - 2019-2020
"""

import numpy as np
from os import listdir
from os.path import isfile, join


def generate_statistics(name, source_repository_path, files_names_list):
    """
    Outputs statistics results.
    """
    print("Statistics for " + name + " repository:")
    lines_numbers_array = []
    chars_numbers_array = []
    
    for file in files_names_list:
        input_file = open(source_repository_path + file, "r", encoding="utf8")
        nb_lines = 1
        nb_chars = 0
        
        line = input_file.readline()
        while line:
            nb_chars += len(line)
            line = input_file.readline()
            nb_lines += 1
        
        lines_numbers_array.append(nb_lines)
        chars_numbers_array.append(nb_chars)
    
    print("\tTotal number of lines: " + str(np.sum(lines_numbers_array)))
    print("\tTotal number of chars: " + str(np.sum(chars_numbers_array)))
    print()
    return (lines_numbers_array, chars_numbers_array)


def compare_to_clean(source_repository_data, clean_data):
    """
    Outputs overall general statistics of files comparison.
    """
    print("Comparing clean to " + source_repository_data[0] + ":")
    
    lines_numbers_difference = np.abs(np.subtract(source_repository_data[1][0], clean_data[0]))
    chars_numbers_difference = np.abs(np.subtract(source_repository_data[1][1], clean_data[1]))
    print("\tMean value of lines: " + str(np.mean(lines_numbers_difference)))
    print("\tStandard deviation of lines: " + str(np.std(lines_numbers_difference)))
    print("\tMean value of chars: " + str(np.mean(chars_numbers_difference)))
    print("\tStandard deviation of chars: " + str(np.std(chars_numbers_difference)))
    print()


def generate_global_statistics(source_repositories_name_and_path, cleaned_repository_path, source_files_repository):
    """
    Allows to generate global statistics of files generated from a specific tool source_repositories_name_and_path
    from sources files in source_files_repository path, compared to an aimed set of files contained in the path
    cleaned_repository_path.
    """
    files_to_extract_content_from = [f for f in listdir(source_files_repository) if isfile(join(source_files_repository, f))]
    
    clean_data = generate_statistics("clean", cleaned_repository_path, files_to_extract_content_from)
    
    other_repositories_data = []
    
    for source_repository_name_and_path in source_repositories_name_and_path:
        other_repositories_data.append((source_repository_name_and_path[0], generate_statistics(source_repository_name_and_path[0], source_repository_name_and_path[1], files_to_extract_content_from)))
    
    for other_repository_data in other_repositories_data:
        compare_to_clean(other_repository_data, clean_data)
    
