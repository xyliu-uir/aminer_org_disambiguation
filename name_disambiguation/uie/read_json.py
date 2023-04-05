import json

#
# with open("/home/liuxunyuan/sort_c_org_not_match_top_1671138959.json", "r") as f:
#     data = json.load(f)
#
# start_rows = 0
# read_rows = 1000
# dataslice = data[start_rows:read_rows]
#
# with open("/home/liuxunyuan/new_org.json","w") as f2:
#     json.dump(dataslice,f2)



def getrows(file, start_rows, end_rows):
    with open(file, "r") as f:
        data = json.load(f)

    start_rows = start_rows
    end_rows = end_rows

    dataslice = data[start_rows:end_rows]

    with open("/home/liuxunyuan/new_org.json","w") as f:
        json.dump(dataslice,f)


# getrows(file="/home/liuxunyuan/sort_c_org_not_match_top_1671138959.json",start_rows=0,end_rows=500)


def get_item(file):
    with open(file, "r") as f:
        org = json.load(f)
    org_list = []
    org_freq = []

    for item in org:
        org_list.append(item[0])
        org_freq.append(item[1])

    return org_list,org_freq

org_list_500,org_freq_500 = get_item('/home/liuxunyuan/new_org.json')

print(org_list_500)
print(type(org_list_500))




#
# with open("/home/liuxunyuan/new_org.json", "r") as f:
#     org = json.load(f)
#
# org_list = []
# org_freq = []
#
# for item in org:
#     org_list.append(item[0])
#     org_freq.append(item[1])
#
# for i in range(len(org_list)):
#     print(org_list[i])






# data = [["Corresponding author.", 736635], ["university of sao paulo", 110371], ["university of liege", 102790], ["Zhejiang University(Zhejiang University),Hangzhou,China", 92871]]
#
# first_items = []
#
# for item in data:
#     first_items.append(item[0])
#
# print(first_items)



#
# first_items = []
#
# for item in data:
#     first_items.append(item[0])
#
# print(first_items)
