import re
import sys, os
import json
from collections import Counter

def get_dic(path):
    f = open(path)
    dic = json.load(f)
    f.close()
    return dic

def get_verdict(GT, EV):
    if GT[0][0]!="N":
        if EV[0][0]!="N":
            verdict = "TP"
        else:
            verdict = "FN"
    else:
        if EV[0][0]!="N":
            verdict = "FP"
        else:
            verdict = "TN"
    return verdict

def store_errors(errors, infos, verdict,annot_GT, annot_eval):
    lg = infos["language"]
    if verdict=="FP":
        errors[verdict].setdefault(lg, [])
        errors[verdict][lg].append(annot_eval)
    elif verdict=="FN":
        errors[verdict].setdefault(lg, [])
        errors[verdict][lg].append(annot_GT)      
#      os.system("gedit %s"%infos["document_path"])
#      dd = input("Next ?")
    return errors

def show_errors(errors):
    for typ, dic in errors.items():
        print("****\n-%s-\n****"%typ)
        for lg, list_errors in dic.items():
            err = Counter(["--".join(x[:1]) for x in list_errors])
            print("-> %s"%lg, err.most_common(5))

def get_measures(dic, beta=1):
    TP, FP, FN = dic["TP"], dic["FP"] , dic["FN"]
    if TP==0:
        return {"Recall":0, "Precision":0, "F%s-measure"%str(beta):0}
    R = float(TP)/(TP+FN)
    P = float(TP)/(TP+FP)
    B = beta*beta
    F = (1+B)*P*R/(B*P+R)
    return {"Recall":round(R,4), "Precision":round(P,4), "F%s-measure"%str(beta):round(F,4)}


# function updated for matching different criterias

# def get_results(dic_GT, dic_eval):
#     dic_results = {x:0 for x in ["TP","FP","FN","TN"]}
#     dic_lg ={}
#     dic_results["Missing_GT"] = []
#     for id_doc, infos in dic_eval.items():
#         lg = infos["language"]
#         dic_lg.setdefault(lg,{x:0 for x in ["TP","FP","FN","TN"]})
#         try:annot_eval = infos["annotations"]
#         except:continue
#         if id_doc in dic_GT:
#             annot_GT = dic_GT[id_doc]["annotations"]  
#             verdict = get_verdict(annot_GT, annot_eval)#TODO: add events
#             dic_results[verdict]+=1
#             dic_lg[lg][verdict]+=1
#         else:
#             dic_results["Missing_GT"].append(id_doc)
#         if verdict=="FP":
#             print(infos["language"],annot_GT, annot_eval)
#       os.system("gedit %s"%infos["document_path"])
#       dd = input("Next ?")
#     if dic_results["TP"]+dic_results["FN"]==0:
#         print("  No relevant documents in this Ground Truth")
#     print(dic_results)
#     print(get_measures(dic_results))
#     print("  %s annotations missing"%str(len(dic_results["Missing_GT"])))
#     for lg , infos in dic_lg.items():
#         print(lg, get_measures(infos))

def get_results(dic_GT, dic_eval, criteria_extraction=None):
    dic_results = {x:0 for x in ["TP","FP","FN","TN"]}
    dic_criteria ={}
    dic_results["Missing_GT"] = []
    for id_doc, infos in dic_eval.items():
        if criteria_extraction == None:
            criteria = infos["language"]
        else:
            criteria = criteria_extraction(infos)
        dic_criteria.setdefault(criteria,{x:0 for x in ["TP","FP","FN","TN"]})
        try:annot_eval = infos["annotations"]
        except:continue
        if id_doc in dic_GT:
            annot_GT = dic_GT[id_doc]["annotations"]  
            verdict = get_verdict(annot_GT, annot_eval)#TODO: add events
            dic_results[verdict]+=1
            dic_criteria[criteria][verdict]+=1
        else:
            dic_results["Missing_GT"].append(id_doc)
#       os.system("gedit %s"%infos["document_path"])
#       dd = input("Next ?")
    if dic_results["TP"]+dic_results["FN"]==0:
        print("  No relevant documents in this Ground Truth")
    measures_by_criteria = {}
    for criteria , infos in dic_criteria.items():
        measures_by_criteria[criteria] = get_measures(infos)
    return (dic_results, get_measures(dic_results), measures_by_criteria)


#  removing default behaviour from original file

# if len(sys.argv)!=3:
#     print("USAGE : arg1=groundtruth file arg2 = result file")
#     exit()
# 
# groundtruth_path = sys.argv[1]
# eval_path = sys.argv[2]
# 
# dic_GT = get_dic(groundtruth_path)
# dic_eval = get_dic(eval_path)
# 
# get_results(dic_GT, dic_eval)
