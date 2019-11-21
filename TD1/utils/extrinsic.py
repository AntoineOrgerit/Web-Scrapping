import numpy as np
import langid
import json
import copy
import subprocess
from os import listdir, remove
from os.path import isfile, join
from utils.daniel.daniel import process
from utils.daniel.evaluate import get_results, get_dic


def print_TP_FP_FN_TN(tools_criterias_data):
    print("TOOLS\t\t|TP\t|FP\t|FN\t|TN")
    print("------------------------------------------------")
    for tool in tools_criterias_data:
        if len(tool) > 7:
            print(tool + "\t|", end="")
        else:
            print(tool + "\t\t|", end="")
        print(str(tools_criterias_data[tool][0]["TP"]) + "\t|" + str(tools_criterias_data[tool][0]["FP"]) + "\t|" + str(tools_criterias_data[tool][0]["FN"]) + "\t|" + str(tools_criterias_data[tool][0]["TN"]))
    print()


def print_FRP(tools_criterias_data, default_header_key):
    print("TOOLS\t\t|\t\tAll\t\t", end="")
    add_spacing = []
    for criteria in tools_criterias_data[default_header_key][2]:
        if len(criteria) >= 24:
            print("|" + criteria+ "\t", end="")
            if len(criteria) >= 31:
                add_spacing.append(criteria)
        elif len(criteria) >= 16:
            print("|\t" + criteria+ "\t", end="")
        elif len(criteria) >= 8:
            print("|\t" + criteria+ "\t\t", end="")
        else:
            print("|\t\t" + criteria+ "\t\t", end="")
    print()
    print("\t\t|\tF\tR\tP\t", end="")
    for criteria in tools_criterias_data[default_header_key][2]:
        print("|\tF\tR\tP\t", end="")
        if criteria in add_spacing:
                print("\t", end="")
    print()
    print("------------------------------------------------", end="")
    for criteria in tools_criterias_data[default_header_key][2]:
        print("--------------------------------", end="")
        if criteria in add_spacing:
                print("--------", end="")
    print()
    for tool in tools_criterias_data:
        if len(tool) > 7:
            print(tool + "\t", end="")
        else:
            print(tool + "\t\t", end="")
        print("|\t" + str(format(tools_criterias_data[tool][1]["F1-measure"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][1]["Recall"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][1]["Precision"], ".2f")) + "\t", end="")
        for criteria in tools_criterias_data[tool][2]:
            print("|\t" + str(format(tools_criterias_data[tool][2][criteria]["F1-measure"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][2][criteria]["Recall"], ".2f")) + "\t" + str(format(tools_criterias_data[tool][2][criteria]["Precision"], ".2f")) + "\t", end="")
            if criteria in add_spacing:
                print("\t", end="")
        print()
    print()


def detect_language(file_path):
    file = open(file_path, "r", encoding="utf8")
    language = langid.classify(file.read())
    file.close()
    return language


def delete_unused_files(clean_repository_json_path, files_to_evaluate):
    clean_repository = json.load(open(clean_repository_json_path, "r", encoding="utf8"))
    for id in list(clean_repository):
        if not clean_repository[id]["path"] in files_to_evaluate:
            clean_repository.pop(id)
    return clean_repository


def prepare_json(json_content, path):
    prepared_json = {}
    for id, infos in json_content.items():
        new_infos = copy.copy(infos)
        new_infos["document_path"] = path + new_infos["path"]
        new_infos["language"] = new_infos["langue"]
        new_infos.pop("langue")
        prepared_json[id] = new_infos
    return prepared_json


def process_corpus():
    out = subprocess.check_output(['python', '../utils/daniel/process_corpus.py',  '-c ../../../exo5/eval.json'])
    composed_out = out.decode('ascii').split("\r\n")
    composed_out = composed_out[len(composed_out) - 2].split("/")
    return composed_out[len(composed_out) - 1]


def evaluate(processed_file, criteria_extraction):
    gold = get_dic('./gold.json')
    eval = get_dic('./' + processed_file)
    return get_results(gold, eval, criteria_extraction)


def perform_extrinsic_evaluation(clean_repository_path_and_json, source_repositories_name_and_path, criteria_extraction, print_header_key=None):
    global_data = {}
    
    for source_repository_name_and_path in source_repositories_name_and_path:
        files_to_evaluate = [f for f in listdir(source_repository_name_and_path[1]) if isfile(join(source_repository_name_and_path[1], f))]
        
        clean_repository = delete_unused_files(clean_repository_path_and_json[1], files_to_evaluate)
        gold_json = prepare_json(clean_repository, clean_repository_path_and_json[0])
        eval_json = prepare_json(clean_repository, source_repository_name_and_path[1])
         
        gold_file = open("./gold.json", "w")
        gold_file.write(json.dumps(gold_json))
        gold_file.close()
        eval_file = open("./eval.json", "w")
        eval_file.write(json.dumps(eval_json))
        eval_file.close()

        processed_file = process_corpus()
        
        global_data[source_repository_name_and_path[0]] = evaluate(processed_file, criteria_extraction)
        
        remove("./gold.json")
        remove("./eval.json")
        remove("./" + processed_file)
    
    print_TP_FP_FN_TN(global_data)
    if print_header_key != None:
        print_FRP(global_data, print_header_key)
    
    return global_data
