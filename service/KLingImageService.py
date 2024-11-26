import json
import logging
import time
import jwt

import requests

from exception.ApiCodeEnum import ApiCodeEnum
from exception.ApiException import ApiException

api_url = "https://api.klingai.com"

logger = logging.getLogger(__name__)


# 鉴权token生成
def encode_jwt_token():
    ak = "871e4d183f4046d3895063bf39fdf035"  # 填写access key
    sk = "05686e6e5b8f4693a6f6c8cd53c87656"  # 填写secret key
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token.decode()


# 可灵服务对接

class KLingImageService:

    def __init__(self):
        self.content_type = "application/json"

    # 创建文生图任务
    def create_image_task(self, prompt):
        path = "/v1/images/generations"
        token = encode_jwt_token()
        headers = {
            'Content-Type': self.content_type,
            'Authorization': 'Bearer ' + token
        }
        req_body = {
            "model": "kling-v1",
            "prompt": prompt,
            "negative_prompt": "",
            "n": 1,  # 生成图片数量
            "aspect_ratio": "16:9",
            "callback_url": ""
        }
        try:
            response = requests.post(api_url + path, headers=headers, json=req_body)
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']
            else:
                logger.warning("[KLing] create generate image task warning! code = %s, message = %s", content['code'], content['message'])
                raise ApiException(ApiCodeEnum.TEXT_TO_IMAGE_ERROR, "[KLing] " + content['message'])
        except Exception as e:
            logger.error("[KLing] create generate image task error!", exc_info=True)
            raise ApiException(ApiCodeEnum.TEXT_TO_IMAGE_ERROR, "[KLing] create generate image task error!")

    # 查询单个文生图任务
    def get_image_task(self, task_id):
        path = "/v1/images/generations/" + task_id
        token = encode_jwt_token()
        headers = {
            'Content-Type': self.content_type,
            'Authorization': 'Bearer ' + token
        }
        try:
            response = requests.get(api_url + path, headers=headers)
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']
            else:
                logger.warning("[KLing] get image task warning! code = %s, message = %s", content['code'], content['message'])
                raise ApiException(ApiCodeEnum.GET_TEXT_IMAGE_ERROR, "[KLing] " + content['message'])
        except Exception as e:
            logger.error("[KLing] get generate image task error!", exc_info=True)
            raise ApiException(ApiCodeEnum.GET_TEXT_IMAGE_ERROR, "[KLing] get generate image task error!")

    # 根据图片创建3D
    def poll_get_image(self, task_id, retry_config):
        """
        轮询获取任务生成的图片
        :param task_id:  任务 ID
        :param retry_config: 轮询的次数和间隔配置
        :return:
        """
        max_image_times = 0
        while True and max_image_times < retry_config['max_image_times']:
            time.sleep(retry_config['each_image_seconds'])
            get_image_task = self.get_image_task(task_id)
            max_image_times += 1
            image_task_status = get_image_task['task_status']
            if image_task_status == 'succeed':
                image_results = get_image_task['task_result']['images']
                return image_results[0]['url']
            if image_task_status == 'failed':
                image_task_message = get_image_task['task_status_msg']
                logger.warning("[KLing] poll get image task warning! status = %s, message = %s", image_task_status, image_task_message)
                raise ApiException(ApiCodeEnum.GET_TEXT_IMAGE_ERROR, image_task_message)
            else:
                logger.info("[KLing] try get image url, retry times = %s!", max_image_times)
        logger.error("[KLing] try get image error! retry times = %s!", max_image_times)
        raise ApiException(ApiCodeEnum.IMAGE_TO_TRIPO_ERROR, "the image url is empty!")
