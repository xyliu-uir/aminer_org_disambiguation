# pip install wudao 请先在终端进行安装，或者到开放平台用户手册中--》》新手指南下载平台调用工具包。
# -*- coding:utf-8 -*-
from wudao.api_request import executeEngineV2, getToken

# 接口API KEY
API_KEY = "77131bab20cb437898b0ffc25c4dc080"
# 公钥
PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKOK5VbfqS8yFC0KedwLnlenhRVs4x7rbqlZQ6viLA9AxSajznMNZQsVcC4E/Bu0UIJ20pFb2xF0IVo4QuCZjmECAwEAAQ=="
# 能力类型
ability_type = "completions"
# 引擎类型
engine_type = "completions_130B"
# 请求参数样例
data = {
    "topP":1,
    "topK":3,
    "temperature":1,
    "lengthPenalty":0.7,
    "minGenLength":50,
    "maxTokens":200,
    "noRepeatNgramSize":3,
    "requestTaskNo":"15859080426360709121",
    "prompt":"问题：冬天，中国哪座城市最适合避寒？问题描述：能推荐一些国内适合冬天避寒的城市吗？回答用户：旅游爱好者 回答："
}

'''
  注意这里仅为了简化编码每一次请求都去获取token， 线上环境token有过期时间， 客户端可自行缓存，过期后重新获取。
'''
token_result = getToken(API_KEY, PUBLIC_KEY)

if token_result and token_result["code"] == 200:
    token = token_result["data"]
    resp = executeEngineV2(ability_type, engine_type, token, data)
    print(resp)
else:
    print("获取token失败，请检查 API_KEY 和 PUBLIC_KEY")