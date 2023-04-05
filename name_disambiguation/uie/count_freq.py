import json
import pandas as pd

# with open("/home/liuxunyuan/sort_c_org_not_match_top_1671138959.json", "r") as f:
#     data = json.load(f)
#
# newdata = list(filter(lambda x: x[1] <= 10, data))
#
# with open('/home/liuxunyuan/PycharmProjects/name_disambiguation/sort_c_org_not_match_freq_under10.json', 'w') as f:
#     json.dump(newdata, f)


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


# org_list, org_freq = get_item("/home/liuxunyuan/PycharmProjects/name_disambiguation/sort_c_org_not_match_freq_under10.json")
# aaa = {'org_list':org_list, 'org_freq':org_freq}
# df = pd.DataFrame(aaa)
# df.to_csv("/home/liuxunyuan/PycharmProjects/name_disambiguation/sort_c_org_not_match_freq_under10.csv")


import pandas as pd

# df = pd.read_csv("./sort_c_org_not_match_freq_over10.csv")
# # print(df)
# freqover10 = df["org_freq"].sum()
# print(freqover10)

df = pd.read_csv("./sort_c_org_not_match_freq_under10.csv")
# print(df)
freqover10 = df["org_freq"].sum()
print(freqover10)

