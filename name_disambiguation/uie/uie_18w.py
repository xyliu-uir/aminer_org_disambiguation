from paddlenlp import Taskflow
from pprint import  pprint
import json
import time
import pandas as pd
import ast
from fill_extract import repl_keywords
from fill_extract import uie2json

with open("data/paper_not_match_top.json") as f:
    data = json.load(f)
# print(type(data))
# print(data[0:10])
# df = pd.DataFrame(data,columns="")
data = repl_keywords(data)
# print(data[0:10])

df = pd.DataFrame(data, columns=["原始"])
df = df['原始']
# print(df.head())
org_list = list(df.values)
# print(len(org_list))

org_uie = []
input_arr = []
prim_org = []


with open("./uie_3_test.txt", "w") as f:
    for i in range(len(org_list)):
        en = org_list[i]
        # print(en)
        schema = ["primary organization", "secondary organization", "tertiary organization", "city", "postal code", "country"]
        ie = Taskflow("information_extraction", schema=schema, model="uie-base-en")
        # print(ie(en))
        uie = ie(en)
        print(uie2json(uie),file = f)


def get_orgs(file):
    """
    The get_orgs function takes in a file and returns two lists:
        1. A list of dictionaries, each dictionary representing the raw text from one line of the input file.
        2. A list of strings, each string representing the primary organization extracted from one line of the input file.

    :param file: Open the file and read it line by line
    :return: A list of the raw text and a list of the primary organizations
    :doc-author: Trelent
    """
    prim_org = []
    raw_text = []

    with open(file, "r") as f:
        for line in f:
            line = ast.literal_eval(line)
            raw_text.append(line)

            if 'primary organization' not in line:
                prim_org.append("none")
                continue
            orgs = line['primary organization']
            max_prob_o = max(orgs, key=lambda x: x['probability'])
            max_prob_o_text = max_prob_o['text']
            # print(max_prob_o_text)
            prim_org.append(max_prob_o_text)

    return raw_text, prim_org

raw_text, prim_org = get_orgs("./uie_3_test.txt")
print(raw_text)
print(prim_org)