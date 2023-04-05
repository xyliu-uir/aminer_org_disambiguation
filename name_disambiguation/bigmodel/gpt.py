import openai

openai.api_key = "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"

def completion(prompt):
    completions = openai.Completion.create(engine = "text-davinci-003", prompt = prompt, max_tokens = 2048, n = 1, stop = None, temperature = 0.5)
    message = completions.choices[0].text
    return message

print(completion("Univ Sci & Technol China, Hefei Natl Lab Phys Sci Microscale, Hefei 230026, Anhui, Peoples R China，提取一级机构，列表格式返回唯一结果"))

