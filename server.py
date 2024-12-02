import logging

from app.SoulHealerAppService import SoulHealerAppService
from database import init_db

logger_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(message)s'
logger = logging.getLogger(__name__)

chat_config = {
    "theme": """你是一个心灵治愈师，能够针对用户的咨询和聊天历史，提供有效的心理开导和回答。""",
    "summary": """你是一个聊天记录分析专家，能够根据用户的聊天记录生成摘要，并识别用户的性格。输出格式为：摘要：<摘要> \n 性格：<性格> \n ，聊天记录为：[%s]""",
    "max_round_size": 100
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=logger_format)
    init_db()
    chat_service = SoulHealerAppService()
    # =============第一轮对话==============================
    answer1 = chat_service.chat_healer("我最近有点不开心，你能帮我吗？")
    print(answer1.content, answer1.summary)
    # =============第二轮对话==============================
    answer2 = chat_service.chat_healer("工作事情太多，干不完")
    print(answer2.content, answer2.summary)
    # =============第三轮对话==============================
    answer3 = chat_service.chat_healer("合作的同事负责的部分老是延期，导致整体进度不符合预期")
    print(answer3.content, answer3.summary)