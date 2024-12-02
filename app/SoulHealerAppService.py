import logging
import os

from exception.ApiException import ApiException
from service.ChatMessageService import ChatMessageService
from service.KLingImageService import KLingImageService
from service.KwaiYiiChatService import KwaiYiiChatService
from service.Tripo3DService import Tripo3DService
from utils.FileUtils import FileUtils
from views.ChatMessageView import ChatMessageView

retry_config = {
    "each_image_seconds": 5,  # 每隔3s轮询一次
    "max_image_times": 20,  # 最多轮询20次
}

chat_config = {
    "theme": """你是一个心灵治愈师，能够针对用户的咨询和聊天历史，提供有效的心理开导和回答。""",
    "summary": """你是一个聊天记录分析专家，能够根据用户的聊天记录生成摘要，并识别用户的性格。输出格式为：摘要：<摘要> \n 性格：<性格> \n ，聊天记录为：[%s]""",
    "max_round_size": 100
}

logger = logging.getLogger(__name__)


# 心灵治愈师app服务
class SoulHealerAppService:

    def __init__(self):
        self.root_path = os.path.abspath(os.path.join(os.getcwd(), "./static"))
        self.kling_service = KLingImageService()
        self.tripo_service = Tripo3DService()
        self.chat_service = KwaiYiiChatService()
        self.message_service = ChatMessageService()

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
        root_dir = self.root_path + "/glb"
        return FileUtils.export_file(file_url, root_dir)

    # 和治愈师聊天
    def chat_healer(self, message):
        if len(message) <= 0:
            return None
        # 查询最近的聊天记录作为聊天历史，按照 id 正序排列
        history = self.message_service.pull_chat_messages(
            pager={
                'page_size': chat_config['max_round_size'],
                'offset': 0
            }
        )
        # 保存发送消息
        session, send_message = self.message_service.save_chat_message(from_role=1, content=message)
        history.append(send_message)
        reply_answer = self.chat_service.do_chat_messages(chat_config=chat_config, messages=history)
        # 保存回复消息
        session, new_answer = self.message_service.save_chat_message(from_role=2, content=reply_answer)
        if new_answer is not None:
            history.append(new_answer)
        # 聊天摘要
        summary = self.chat_service.do_chat_summary(chat_config, history)
        self.message_service.update_session_summary(user_id=0, session_id=session.id, summary=summary, new_message=new_answer)
        return None if new_answer is None else ChatMessageView(new_answer, summary)

    # 分页查询聊天记录
    def pull_messages(self, pager):
        messages = self.message_service.pull_chat_messages(pager=pager)
        data_list = list()
        for message in messages:
            data_list.append(ChatMessageView(message, None).to_dict())
        return data_list
