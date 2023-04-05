# gui_yi_table = {"technol": "technology",
#                 "tech": "technology",
#                 "telecommun": "telecommunications",
#                 "telecom": "telecommunications",
#                 "phys": "physics",
#                 "appl": "apply",
#                 "acad": "academy",
#                 "automot": "automotive",
#                 "hlth": "health",
#                 "agr": "agricultural",
#                 "coll": "college",
#                 "sci": "sciences",
#                 "med": "medicine",
#                 "natl": "national",
#                 "cas": "chinese academy of sciences",
#                 "hosp": "hospital",
#                 "prov": "province",
#                 "inst": "institute",
#                 "ctr": "center",
#                 "lab": "laboratory",
#                 "cent": "central",
#                 "res": "research",
#                 "grp": "group",
#                 "petr": "petroleum",
#                 "mat": "materials",
#                 "gen": "general",
#                 "met": "metals",
#                 "&": "and",
#                 "aeronaut": "aeronautics",
#                 "astronaut": "astronautics",
#                 "clin": "clinic",
#                 "engn": "engineering",
#                 "dept": "department",
#                 "univ": "university",
#                 'technol,': 'technology,',
#                 'tech,': 'technology,',
#                 'telecommun,': 'telecommunications,',
#                 'telecom,': 'telecommunications,',
#                 'phys,': 'physics,',
#                 'appl,': 'apply,',
#                 'acad,': 'academy,',
#                 'automot,': 'automotive,',
#                 'hlth,': 'health,',
#                 'agr,': 'agricultural,',
#                 'coll,': 'college,',
#                 'sci,': 'sciences,',
#                 'med,': 'medicine,',
#                 'natl,': 'national,',
#                 'cas,': 'chinese academy of sciences,',
#                 'hosp,': 'hospital,',
#                 'prov,': 'province,',
#                 'inst,': 'institute,',
#                 'ctr,': 'center,',
#                 'lab,': 'laboratory,',
#                 'cent,': 'central,',
#                 'res,': 'research,',
#                 'grp,': 'group,',
#                 'petr,': 'petroleum,',
#                 'mat,': 'materials,',
#                 'gen,': 'general,',
#                 'met,': 'metals,',
#                 '&,': 'and,',
#                 'aeronaut,': 'aeronautics,',
#                 'astronaut,': 'astronautics,',
#                 'clin,': 'clinic,',
#                 'engn,': 'engineering,',
#                 'dept,': 'department,',
#                 'univ,': 'university,'}
#
#
# lst = ["university of sao paulo", "Univ Calif San Francisco", "Baylor Coll Med, Houston", "Fermilab Natl Accelerator Lab","Chinese Acad Sci, Inst Phys, Beijing Natl Lab Condensed Matter Phys, Beijing 100190, Peoples R China"]
#
#
# def repl_keywords(lst):
#     for i in range(len(lst)):
#         words = lst[i].lower().split() # 按空格或者逗号分割字符串
#         for j in range(len(words)):
#             if words[j].lower() in gui_yi_table: # 判断是否在gui_yi_table的键中出现
#                 words[j] = gui_yi_table[words[j].lower()] # 如果在，将其替换为gui_yi_table中对应的值
#         lst[i] = " ".join(words) # 将分割后的单词重新拼接回原字符串
#     return lst
#
# print(repl_keywords(lst=lst))
from paddlenlp import Taskflow
from pprint import pprint
import json
import time
import pandas as pd
import ast

def get_orgs(file):
    prim_org = []
    raw_text = []

    with open(file, "r") as f:
        for line in f:
            line = ast.literal_eval(line)
            if line[0] == '[' and line[-1] == ']':
                line = line[1:-1]
            raw_text.append(line)

            if 'primary organization' not in line:
                prim_org.append("NaN")
                continue
            orgs = line['primary organization']
            max_prob_o = max(orgs, key=lambda x: x['probability'])
            max_prob_o_text = max_prob_o['text']
            # print(max_prob_o_text)
            prim_org.append(max_prob_o_text)

    return raw_text, prim_org

raw_text, prim_org = get_orgs("./top_1000_uie.txt")
print(raw_text)

