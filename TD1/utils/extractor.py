from os import listdir
from os.path import isfile, join
from inspect import signature

def extract(source_repository_path, destination_repository_path, specific_treatement_function):
    files_to_extract_content_from = [f for f in listdir(source_repository_path) if isfile(join(source_repository_path, f))]
    
    for file_to_extract_content_from in files_to_extract_content_from:
        input_file = open(source_repository_path + file_to_extract_content_from, "r", encoding="utf8", errors="replace")
        output_file = open(destination_repository_path + file_to_extract_content_from, "w", encoding="utf8")
        
        if len(signature(specific_treatement_function).parameters) == 2:
            specific_treatement_function(input_file, output_file)
        else:
            specific_treatement_function(input_file, output_file, file_to_extract_content_from)
        
        output_file.close()
        input_file.close()
