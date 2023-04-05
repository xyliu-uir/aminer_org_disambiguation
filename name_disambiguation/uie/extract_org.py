from paddlenlp import Taskflow
from pprint import pprint
import json
import time
import pandas as pd
import ast

gui_yi_table = {"technol": "technology",
                "tech": "technology",
                "telecommun": "telecommunications",
                "telecom": "telecommunications",
                "phys": "physics",
                "appl": "apply",
                "acad": "academy",
                "automot": "automotive",
                "hlth": "health",
                "agr": "agricultural",
                "coll": "college",
                "sci": "sciences",
                "med": "medicine",
                "natl": "national",
                "cas": "chinese academy of sciences",
                "hosp": "hospital",
                "prov": "province",
                "inst": "institute",
                "ctr": "center",
                "lab": "laboratory",
                "cent": "central",
                "res": "research",
                "grp": "group",
                "petr": "petroleum",
                "mat": "materials",
                "gen": "general",
                "met": "metals",
                "&": "and",
                "aeronaut": "aeronautics",
                "astronaut": "astronautics",
                "clin": "clinic",
                "engn": "engineering",
                "dept": "department",
                "univ": "university"}


def replace_keywords():
    org_list, org_freq = get_item("./")
    # print(org_list,org_freq)
    for key in gui_yi_table:
        org_list_fill = [o.replace(key, gui_yi_table.get(key, key)) for o in org_list]
    # print(org_list_fill)

    return org_list_fill, org_freq


def get_rows(file, start_rows, end_rows, save_file):
    """
    它需要一个 json 文件，并返回一个包含你想要的行的新 json 文件

    :param file: 您要切片的文件
    :param start_rows: 您要开始的行号
    :param end_rows: 要从原始文件中获取的行数
    """
    with open(file, "r") as f:
        data = json.load(f)

    start_rows = start_rows
    end_rows = end_rows

    dataslice = data[start_rows:end_rows]

    with open(save_file, "w") as f:
        json.dump(dataslice, f)


'''只执行一次'''


# get_rows(file="/home/liuxunyuan/sort_c_org_not_match_top_1671138959.json",
#          start_rows=0,
#          end_rows=500,
#          save_file="/home/liuxunyuan/new_org.json")


def get_item(file):
    """
    它打开文件，读取文件，并返回组织列表及其频率

    :param file: json文件的文件名
    :return: 组织列表和组织频率列表。
    """
    with open(file, "r") as f:
        org = json.load(f)
    org_list = []
    org_freq = []

    for item in org:
        org_list.append(item[0])
        org_freq.append(item[1])

    return org_list, org_freq


def clean_data(text):
    """
    - 小写
    - 删除主题标签
    - 删除 URL 地址
    - 消除 @
    - 删除标点符号
    - 删除多余的空格
    - 删除引号

    :param text: 要清理的文本
    :return: 清理后的文字。
    """
    text = text.lower()  # lowercase
    text = text.replace(r"\#", "")  # replaces hashtags
    text = text.replace(r"http\S+", "URL")  # remove URL addresses
    text = text.replace(r"@", "")
    text = text.replace(r"[^A-Za-z0-9()!?\'\`\"]", " ")
    text = text.replace("\s{2,}", " ")
    text = text.replace(r"^\"|\"$", " ")
    return text


def create_org_csv(orgin_path, target_path):
    """
    此函数接受原始 csv 文件和目标 csv 文件，然后它将使用清理后的数据创建一个新的 csv 文件

    :param orgin_path: 原始csv文件的路径
    :param target_path: 将创建的 csv 文件的路径
    """
    org_list_500, org_freq_500 = get_item(orgin_path)

    org_list_500_cleaned = [clean_data(org_list_500[i]) for i in range(len(org_list_500))]

    org = {'prev': org_list_500, 'after': org_list_500_cleaned}
    df = pd.DataFrame(org)
    df.to_csv(target_path, index=False)


'''只执行一次'''


# create_org_csv(orgin_path='/home/liuxunyuan/new_org.json',target_path="./Organizations500.csv")


def extract(file, task, model, extracted_path):
    """
    它读入一个 csv 文件，删除“prev”列，将“after”列重命名为“Organizations”，然后遍历数据框的前 100 行，从每一行中提取组织

    :param file: 包含数据的文件的路径
    :param task: 您要执行的任务。在这种情况下，它是“提取物”
    :param model: 用于任务的模型。
    """
    schema = ["primary organization", "secondary organization", "tertiary organization", "city", "postal code",
              "country"]
    df = pd.read_csv(file)
    df = df.drop("prev", axis=1)
    df = df.rename(columns={"after": "Organizations"}, inplace=False)
    with open(extracted_path, "w") as f:
        for i in range(10):
            en = df.values[i][0]
            ie = Taskflow(task, model, schema=schema)
            extracted = ie(en)
            print(extracted, file=f)


# extract(file="./Organizations500.csv", task="information_extraction", model="uie-base-en", extracted_path="./raw_org_extracted.json")


def get_items(file):
    """
    It opens the file, reads each line, and then extracts the information we need
    :return: the maximum probability of the organization, postal code, country and city.
    """

    prim_org = []
    raw_text = []
    post_code = []
    countries = []
    cities = []

    with open(file, "r") as f:
        for line in f:
            line = ast.literal_eval(line)
            # print(line)
            raw_text.append(line)

            if 'primary organization' not in line:
                prim_org.append("NaN")
                continue
            orgs = line['primary organization']
            max_prob_o = max(orgs, key=lambda x: x['probability'])
            max_prob_o_text = max_prob_o['text']
            # print(max_prob_o_text)
            prim_org.append(max_prob_o_text)

            if 'postal code' not in line:
                post_code.append("NaN")
                continue
            zip_code = line['postal code']
            max_prob_p = max(zip_code, key=lambda x: x['probability'])
            max_prob_p_text = max_prob_p['text']
            # print(max_prob_p_text)
            post_code.append(max_prob_p_text)

            if 'country' not in line:
                countries.append("NaN")
                continue
            country = line['country']
            max_prob_c = max(country, key=lambda x: x['probability'])
            max_prob_c_text = max_prob_c['text']
            # print(max_prob_c_text)
            countries.append(max_prob_c_text)

            if 'city' not in line:
                cities.append("NaN")
                continue
            city = line['city']
            max_prob_ci = max(city, key=lambda x: x['probability'])
            max_prob_ci_text = max_prob_ci['text']
            # print(max_prob_ci_text)
            cities.append(max_prob_ci_text)

    return raw_text, prim_org, post_code, countries, cities


raw_text, prim_org, post_code, countries, cities = get_items(file="./raw_org_extracted.txt")
# # print(prim_org)
# # print(post_code)
# # print(countries)
# # print(cities)
#
#
org_list, org_freq = get_item("/home/liuxunyuan/new_org.json")
org_list_fill, _ = replace_keywords()
print(len(raw_text), len(prim_org), len(post_code), len(countries), len(cities), len(org_list), len(org_list_fill), len(org_freq))

# dataf = {
#     "Origin text": org_list,
#     "Text after filling": org_list_fill,
#     "Term frequency": org_freq,
#     "Raw text": raw_text,
#     "Primary organizations": prim_org
# }
# # #
# df = pd.DataFrame(dataf)
# # print(df.head())
# # #
# df.to_csv("./Primary Organizations.csv")

# print(max_prob_o_text)
# with open('result.txt') as f1:
#     with open('./extracted.txt', 'w') as f2:
#         for line in f1.readlines():
#             en = line.strip()
#             schema = ['Country of origin','Country of sale','Weapon type', 'Supplier', 'Distributor', "Producer", "Manufacturer", "Cost"]
#             ie = Taskflow('information_extraction', model='uie-base-en', schema=schema)
#             print(ie(en), file=f2)


# df = pd.read_csv("./Organizations500.csv")
# # print(df.head())
# df = df.drop("prev", axis=1)
# df = df.rename(columns={"after": "Organizations"}, inplace=False)
# # print(df.head())
#
# for i in range(len(df)):
#     print(df.values[i][0])
#
# schema = ["primary organization", "secondary organization", "tertiary organization", "city", "postal code", "country"]
# en = df.values[3][0]
# ie = Taskflow('information_extraction', model="uie-base-en", schema=schema)
# pprint(ie(en))


# print(df.values[1])


# def extact_txt(file):
#     with open(file) as f:
#         for line in f.readlines():
#             en = line.strip()
#             schema = ["Primary organization", "secondary organization", "tertiary organization", "city", "postal code",
#                       "country"]
#             ie = Taskflow('information_extraction', model='uie-base-en', schema=schema)
#             pprint(ie(en))

# extact_txt('')





# replace_keywords()
