import asyncio
import json
import logging
import traceback

import requests
import websockets

from exception.ApiCodeEnum import ApiCodeEnum
from exception.ApiException import ApiException

api_url = "https://api.tripo3d.ai/v2/openapi"
api_key = "tsk_vtHuUP6fuDEcQa5iXS591SgiWr1hv4-nKvlvxASGLTP"

logger = logging.getLogger(__name__)


class Tripo3DService:
    def __init__(self):
        self.content_type = "application/json"

    # 将url中的文件直接转为3D模型
    def generation_image(self, file_url):
        data = {
            "type": "image_to_model",
            "model_version": "v2.0-20240919",
            "file": {
                "type": "png",
                "url": file_url
            }
        }
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f"Bearer {api_key}"
        }
        try:
            response = requests.post(api_url + "/task", headers=headers, json=data)
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']
            else:
                code = content['code']
                message = content['message']
                print(content)
                raise ApiException(ApiCodeEnum.IMAGE_TO_TRIPO_ERROR, f"[Tripo] generate 3D file error! code = {code}, message = {message}")
        except Exception as e:
            traceback.print_exc()
            raise ApiException(ApiCodeEnum.IMAGE_TO_TRIPO_ERROR, "[Tripo] generate 3D file error!")

    def get_image_task(self, task_id):
        path = "/task/" + task_id
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        try:
            response = requests.get(api_url + path, headers=headers)
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']
            else:
                code = content['code']
                message = content['message']
                print(content)
                raise ApiException(ApiCodeEnum.GET_TRIPO_FILE_ERROR, f"[Tripo] get 3D file error!! code = {code}, message = {message}")
        except Exception as e:
            traceback.print_exc()
            raise ApiException(ApiCodeEnum.GET_TRIPO_FILE_ERROR, "[Tripo] get 3D file error!")

    async def watch_image_task(self, task_id):
        wss_url = f"wss://api.tripo3d.ai/v2/openapi/task/watch/{task_id}"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        async with websockets.connect(wss_url, extra_headers=headers) as websocket:
            while True:
                message = await websocket.recv()
                try:
                    data = json.loads(message)
                    status = data['data']['status']
                    if status not in ['running', 'queued']:
                        break
                except json.JSONDecodeError:
                    print("Received non-JSON message:", message)
                    break
        return data['data']

    def get_watch_image(self, task_id):
        logger.info("start watch image stream! task_id = %s", task_id)
        tripo_image = asyncio.new_event_loop().run_until_complete(
            self.watch_image_task(task_id)
        )
        logger.info("finish watch image stream! task_id = %s", task_id)
        tripo_image_status = tripo_image['status']
        if tripo_image_status == 'success':
            return tripo_image['output']['pbr_model']
        if tripo_image_status in ['failed', 'unknown', 'cancelled']:
            print(tripo_image)
            raise ApiException(ApiCodeEnum.GET_TRIPO_FILE_ERROR, "get tripo image 3D failed!")
        raise ApiException(ApiCodeEnum.GET_TRIPO_FILE_ERROR, "the 3D file url is empty!")
