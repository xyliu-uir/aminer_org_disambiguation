import pandas as pd
import requests
import openai
import re


proxies = {
    'https': 'https://lum-customer-hl_451b22ff-zone-static:edw22l2gkrf2@zproxy.lum-superproxy.io:22225',
    'http': 'http://lum-customer-hl_451b22ff-zone-static:edw22l2gkrf2@zproxy.lum-superproxy.io:22225',
}


def gpt_post(msg):
    key = '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'
    # url = "https://api.openai.com/v1/chat/completions"
    url = "https://api.openai.com/v1/completions"
    try:
        resp = requests.post(url, json={
            # 'model': 'gpt-3.5-turbo',
            'model': 'text-davinci-003',
            'messages': [
                {"role": "user", "content": msg.replace('\n', ' ')}
            ],
        }, headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }, proxies=proxies)
        print(resp.json()['choices'][0]['message']['content'])
        gpt
    except ConnectionResetError as e:
        print(e)
        gpt_post(msg)
    except requests.exceptions.ProxyError as e:
        print(e)
        gpt_post(msg)





def gpt():
    df = pd.read_csv("../output/sort_c_org_not_match_top_1000_cleaned.csv")

    openai.api_key = "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"


    df = df["Filled"]
    org_list = list(df.values)
    org_gpt = []
    inputa = []

    def completion(prompt):
        completions = openai.Completion.create(engine = "text-davinci-003", prompt = prompt, max_tokens = 2048, n = 1, stop = None, temperature = 0.5)
        message = completions.choices[0].text
        return message

    prompt = "Extract primary organization and return unique results in list format"
    for i in range(10):
        input = org_list[i]
        inputa.append(input)
        data = input + prompt
        item_gpt = completion(data)
        item_gpt = re.sub(r"\n", "", item_gpt)
        print(item_gpt)
        org_gpt.append(item_gpt)

        
    org = {'input': inputa, 'org_gpt': org_gpt}
    df = pd.DataFrame(org)
    # print(df.head())
    df.to_csv("../output/org_gpt.csv")
