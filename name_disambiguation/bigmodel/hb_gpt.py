import openai
import requests
import os

proxies = {
    'https': 'https://lum-customer-hl_451b22ff-zone-static:edw22l2gkrf2@zproxy.lum-superproxy.io:22225',
    'http': 'http://lum-customer-hl_451b22ff-zone-static:edw22l2gkrf2@zproxy.lum-superproxy.io:22225',
}

def chatAPi(list_a):
    # Your OpenAI API Key
    api_key = "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"
    # The text prompt you want to generate a response
    # input_prompt = input("清华大学是哪个城市的")
    num = 0
    # prompt = ''
    url = "https://api.openai.com/v1/chat/completions"
    # url = "https://api.openai.com/v1/completions"
    # The headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    for i in list_a:
        prompt = 'Extract primary organization and return unique results in list format %s' %i
        data = {
            "model": "gpt-3.5-turbo",
            # "model": "text-davinci-003",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.7,
            "frequency_penalty": 0,
            "presence_penalty": 0}
        # Make the API request
        response = requests.post(url, headers=headers, json=data, proxies=proxies)
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the generated text from the response
            generated_text = response.json()['choices'][0]['message']['content']
            print(generated_text)
        else:
            # Handle the error
            print(f"Request failed with status code 额{response.status_code}")
    num = 0
    openai.api_key = os.getenv(api_key)
    # The URL for OpenAI's API
    return


chatAPi(['School of Resource and Environmental Science,Wuhan University,Wuhan,Hubei'])