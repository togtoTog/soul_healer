import requests
import json
import time

from meta_data import *

# 相似图

def draw_simillar_pic_prepare(prompt, pic_key):
    url = domain + '/vcg/similarImageGenerate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    params = {
    }
    timestamp_millis = int(time.time() * 1000)
    json_data = {
        "image": {
            "custom_request_header": {},
            "bucket_name": bucket_name,
            "db": db,
            "table": table,
            "key": pic_key
        },
        "vcg_common_request": {
            "biz": ketu_biz,
            "request_type": 1,
            "create_time": timestamp_millis,
            "bucket_name": bucket_name,
            "task_id": "",
            "params": {},
            "request_id": "unique_id"
        },
        "strength":"Number",
        "seed": [],
        "negative_prompt": "",
        "width": 1024,
        "image_count": 1,
        "fidelity": 0.5,
        "style": "",
        "prompt": prompt,
        "height": 1024
    }
    response = requests.post(url, params=params, headers=headers, json=json_data)
    json_response = json.loads(response.content)
    task_id = json_response['vcg_common_response']['task_id']
    return task_id


def draw_simillar_pic(task_id, prompt, pic_key):
    url = domain + '/vcg/similarImageGenerate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    params = {
    }
    timestamp_millis = int(time.time() * 1000)
    json_data = {
        "image": {
            "custom_request_header": {},
            "bucket_name": bucket_name,
            "db": db,
            "table": table,
            "key": pic_key
        },
        "vcg_common_request": {
            "biz": ketu_biz,
            "request_type": 2,
            "create_time": timestamp_millis,
            "bucket_name": bucket_name,
            "task_id": task_id,
            "params": {},
            "request_id": "unique_id"
        },
        "seed": [],
        "negative_prompt": "",
        "width": 1024,
        "image_count": 1,
        "fidelity": 0.5,
        "style": "",
        "prompt": prompt,
        "height": 1024
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

