import logging
import os
from utils.FileUtils import FileUtils
from exception.ApiException import ApiException
from service.KLingImageService import KLingImageService
from service.Tripo3DService import Tripo3DService

retry_config = {
    "each_image_seconds": 5,  # 每隔3s轮询一次
    "max_image_times": 20,  # 最多轮询20次
}

logger = logging.getLogger(__name__)


# 心灵治愈师app服务
class SoulHealerAppService:

    def __init__(self):
        self.kling_service = KLingImageService()
        self.tripo_service = Tripo3DService()

    # 创建1个心灵治愈师
    def create_soul_healer(self, prompt):
        try:
            # 创建文本生成图片任务
            create_image_task = self.kling_service.create_image_task(prompt)
            # 轮询，获取生成的图片
            image_url = self.kling_service.poll_get_image(create_image_task['task_id'], retry_config)
            logger.info("create image success! image_url: %s", image_url)
            # 创建图片生成3D模型任务
            tripo_image = self.tripo_service.generation_image(image_url)
            # 监听ws获取3D模型文件
            tripo_image_url = self.tripo_service.get_watch_image(tripo_image['task_id'])
            logger.info("create 3D file success! tripo_url: %s", tripo_image_url)
            return tripo_image_url
        except ApiException as e:
            logger.error("create soul healer error! prompt: %s", prompt, exc_info=True)
            raise e

    # 导出3D文件
    def export_soul_healer(self, file_url):
        root_dir = os.path.abspath(os.path.join(os.getcwd(), "./static/glb"))
        return FileUtils.export_file(file_url, root_dir)