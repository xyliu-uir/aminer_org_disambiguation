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
                "univ": "university",
                'technol,': 'technology,',
                'tech,': 'technology,',
                'telecommun,': 'telecommunications,',
                'telecom,': 'telecommunications,',
                'phys,': 'physics,',
                'appl,': 'apply,',
                'acad,': 'academy,',
                'automot,': 'automotive,',
                'hlth,': 'health,',
                'agr,': 'agricultural,',
                'coll,': 'college,',
                'sci,': 'sciences,',
                'med,': 'medicine,',
                'natl,': 'national,',
                'cas,': 'chinese academy of sciences,',
                'hosp,': 'hospital,',
                'prov,': 'province,',
                'inst,': 'institute,',
                'ctr,': 'center,',
                'lab,': 'laboratory,',
                'cent,': 'central,',
                'res,': 'research,',
                'grp,': 'group,',
                'petr,': 'petroleum,',
                'mat,': 'materials,',
                'gen,': 'general,',
                'met,': 'metals,',
                '&,': 'and,',
                'aeronaut,': 'aeronautics,',
                'astronaut,': 'astronautics,',
                'clin,': 'clinic,',
                'engn,': 'engineering,',
                'dept,': 'department,',
                'univ,': 'university,',
                'chem': 'chemical',
                'chem,': 'chemical,'}


def get_rows(file, start_rows, end_rows, save_file):
    """
    The get_rows function takes in a file, start_rows, end_rows and save_file as arguments.
    It then opens the file and loads it into a json object. It then slices the data from
    start rows to end rows (inclusive) and saves that slice to save_file.

    :param file: Specify the file to be read
    :param start_rows: Tell the function where to start slicing the data
    :param end_rows: Specify the last row of data to be included in the new file
    :param save_file: Save the data to a new file
    :return: A slice of the data from start_rows to end_rows
    """
    with open(file, "r") as f:
        data = json.load(f)

    start_rows = start_rows
    end_rows = end_rows

    dataslice = data[start_rows:end_rows]

    with open(save_file, "w") as f:
        json.dump(dataslice, f)


# get_rows(file="/home/liuxunyuan/sort_c_org_not_match_top_1671138959.json",
#          start_rows=0,
#          end_rows=1000,
#          save_file="/home/liuxunyuan/PycharmProjects/name_disambiguation/sort_c_org_not_match_top_1000.json")


def clean_data(text):
    """
    The clean_data function takes in a string of text and performs the following: 1. Lowercases the text 2. Replace
    hashtags with an empty string (i.e., removes them) 3. Removes URL addresses by replacing them with
    &quot;URL&quot; 4. Removes @ mentions by replacing them with an empty string (i.e., removes them) Note that this
    will also remove @ mentions from within words, e.g., &quot;@mentionable&quot; -&gt; &quot;mentionable&quot;.
    This is fine for our purposes here, but may not be ideal in other contexts where you want

    :param text: Pass in the text that is to be cleaned
    :return: A string
    """
    text = text.lower()  # lowercase
    text = text.replace(r"\#", "")  # replaces hashtags
    text = text.replace(r"http\S+", "URL")  # remove URL addresses
    text = text.replace(r"@", "")
    text = text.replace(r"[^A-Za-z0-9()!?\'\`\"]", " ")
    text = text.replace("\s{2,}", " ")
    text = text.replace(r"^\"|\"$", " ")
    return text


def get_item(file):
    """
    The get_item function takes in a file and returns two lists:
        1. A list of the organizations that are mentioned in the file
        2. A list of how many times each organization is mentioned

    :param file: Specify the file that you want to read from
    :return: The list of organizations and the frequency of each organization
    """
    with open(file, "r") as f:
        org = json.load(f)
    org_list = []
    org_freq = []

    for item in org:
        org_list.append(item[0])
        org_freq.append(item[1])

    return org_list, org_freq


def repl_keywords(lst):
    """
    The repl_keywords function takes a list of strings as input and returns the same list with all keywords replaced.
    The function first splits each string into words, then checks if any word is in the gui_yi_table dictionary. If
    so, it replaces that word with its corresponding value from gui_yi_table.

    :param lst: Store the list of strings
    :return: A list of strings
    :doc-author: Trelent
    """
    for i in range(len(lst)):
        words = lst[i].lower().split()  # 按空格或者逗号分割字符串
        for j in range(len(words)):
            if words[j].lower() in gui_yi_table:  # 判断是否在gui_yi_table的键中出现
                words[j] = gui_yi_table[words[j].lower()]  # 如果在，将其替换为gui_yi_table中对应的值
        lst[i] = " ".join(words)  # 将分割后的单词重新拼接回原字符串
    return lst


def create_org_csv(origin_path, target_path):
    """
    The create_org_csv function takes in two arguments:
        1. origin_path - the path to the original csv file containing all the organizations
        2. target_path - where you want to save your new csv file with cleaned data

    :param origin_path: Specify the path of the original data
    :param target_path: Specify the location of where the csv file will be saved
    :return: A csv file with two columns
    """
    org_list_1000, org_freq_1000 = get_item(origin_path)

    org_list_1000_cleaned = [clean_data(org_list_1000[i]) for i in range(len(org_list_1000))]

    filled = repl_keywords(org_list_1000)

    org = {'Origin Organizations': org_list_1000, 'Cleaned': org_list_1000_cleaned, 'Filled': filled}
    df = pd.DataFrame(org)
    df.to_csv(target_path, index=False)


# create_org_csv(origin_path="./sort_c_org_not_match_top_1000.json",
#                target_path="./sort_c_org_not_match_top_1000_cleaned.csv")




def uie2json(uie):
    """
    The uie2json function takes a uie object and converts it to json.

    :param uie: Pass in the data that is to be converted into json format
    :return: A json object
    """
    jsondata = str(uie)
    if jsondata[0] == '[' and jsondata[-1] == ']':
        jsondata = jsondata[1:-1]
    jsondata = json.dumps(jsondata)
    jsondata = json.loads(jsondata)
    jsondata = jsondata.replace("'", '"')
    return jsondata


def save_raw_txt():
    """
    The save_raw_txt function saves the raw text of the top 1000 companies in a txt file.
        The function is used to save time when running information extraction on all of the
        top 1000 companies.

    :return: A list of dictionaries, each dictionary representing a single extracted entity
    """
    with open("./top_1000_uie.txt", "w") as f:
        schema = ["primary organization", "secondary organization", "tertiary organization", "city", "postal code",
                  "country"]
        df = pd.read_csv("./sort_c_org_not_match_top_1000_cleaned.csv")
        df = df["Filled"]
        for i in range(len(df)):
            en = df.values[i]
            ie = Taskflow("information_extraction", schema=schema, model="uie-base-en")
            uie = ie(en)
            print(uie2json(uie=uie), file=f)


# save_raw_txt()




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


# raw_text, prim_org = get_orgs("./top_1000_uie.txt")
# org_list, org_freq = get_item(file="./sort_c_org_not_match_top_1000.json")
# df = pd.read_csv("./sort_c_org_not_match_top_1000_cleaned.csv")
# df["Term Frequency"] = org_freq
# df["Primary Organization"] = prim_org
# print(df.head())
# df.to_csv("./Result.csv")

# df = pd.read_csv("./Result.csv")
# df = df['Primary Organization']
# print(list(df.values))




