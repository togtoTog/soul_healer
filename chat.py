import requests
import json
import random

from meta_data import *

# 聊天
# 入参：question--问题，original_history--对话历史
# 出参：answer--答案，query_history--加上答案的新的对话历史
def chat(question, original_history):
    token = access_token
    url = domain + '/kwaiyii/chat'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    params = {
    }
    random_num = random.randint(0, 200)
    print("random_num:" + str(random_num))
    json_data = {
        'req_id': '1',
        'query_history': original_history,
        'biz': kwaiyi_biz,
        'query': question,
        'session_id': '1',
        'config': {
            'random_seed': random_num
        }
    }
    response = requests.post(url, params=params, headers=headers, json=json_data)
    json_response = json.loads(response.content)
    print(json_response)
    answer = json_response['answer']
    query_history = json_response['query_history']
    return answer, query_history