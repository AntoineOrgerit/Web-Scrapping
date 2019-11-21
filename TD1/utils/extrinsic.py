import numpy as np
import json
import copy
import subprocess
from os import listdir, remove
from os.path import isfile, join


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
        new_infos["path"] = path + new_infos["path"]
        new_infos["language"] = new_infos["langue"]
        new_infos.pop("langue")
        prepared_json[id] = new_infos
    return prepared_json


def perform_extrinsic_evaluation(clean_repository_path_and_json, source_repositories_name_and_path, criteria_extraction, print_header_key=None):
    for source_repository_name_and_path in source_repositories_name_and_path:
        files_to_evaluate = [f for f in listdir(source_repository_name_and_path[1]) if isfile(join(source_repository_name_and_path[1], f))]
        
        clean_repository = delete_unused_files(clean_repository_path_and_json[1], files_to_evaluate)
        gold_json = prepare_json(clean_repository, clean_repository_path_and_json[0])
        eval_json = prepare_json(clean_repository, source_repository_name_and_path[1])
        print(gold_json[next(iter(gold_json))]["path"])
        print(eval_json[next(iter(eval_json))]["path"])
        
        gold_file = open("./gold.json", "w")
        gold_file.write(json.dumps(gold_json))
        gold_file.close()
        eval_file = open("./eval.json", "w")
        eval_file.write(json.dumps(eval_json))
        eval_file.close()
        
        out = subprocess.check_output(['python', '../utils/daniel/evaluate.py',  './gold.json', './eval.json'])
        remove("./gold.json")
        remove("./eval.json")
        
        print(out)
        composed_out = out.decode('ascii').split("\r\n")
        for specific_out in composed_out:
            print(specific_out)
