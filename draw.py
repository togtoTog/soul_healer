import requests
import json
import time

from meta_data import *

# 文生图

# 提交图片生成任务，异步任务
def draw_prepare(prompt):
    url = domain + '/vcg/textToImage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    params = {
    }
    timestamp_millis = int(time.time() * 1000)
    json_data = {
        "prompt": prompt,
        "negative_prompt": "",
        "image_count": 1,
        "seed": [],
        "width": 1024,
        "height": 1024,
        "style": "",
        "vcg_common_request": {
            "biz": ketu_biz,
            "request_id": "unique_id",
            "request_type": 1,
            "task_id": "",
            "params": {
                "callBackKey": "callBackValue"
            },
            "create_time": timestamp_millis,
            "bucket_name": bucket_name
        }
    }
    response = requests.post(url, params=params, headers=headers, json=json_data)
    json_response = json.loads(response.content)
    task_id = json_response['vcg_common_response']['task_id']
    return task_id

# 查询进度，返回结果码和图片的key
def draw(task_id, prompt):
    url = domain + '/vcg/textToImage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    params = {
    }
    timestamp_millis = int(time.time() * 1000)
    json_data = {
        "prompt": prompt,
        "negative_prompt": "",
        "image_count": 1,
        "seed": [],
        "width": 1024,
        "height": 1024,
        "style": "",
        "vcg_common_request": {
            "biz": ketu_biz,
            "request_id": "unique_id",
            "request_type": 2,
            "task_id": task_id,
            "params": {},
            "create_time": timestamp_millis,
            "bucket_name": bucket_name
        }
    }
    response = requests.post(url, params=params, headers=headers, json=json_data)
    json_response = json.loads(response.content)
    result_code = json_response['vcg_common_response']['result_code']
    generate_image_infos = json_response['generate_image_infos']
    keys = []
    if result_code != 0:
        return result_code, keys
    # print(generate_image_infos)
    for item in generate_image_infos:
        if 'image' in item:
            keys.append(item['image']['key'])
    return result_code, keys


