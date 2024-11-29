import logging
import sys

from app.SoulHealerAppService import SoulHealerAppService
from database import init_db
from service.ChatMessageService import ChatMessageService

logger_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(message)s'
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    print(sys.getdefaultencoding())
    logging.basicConfig(level=logging.INFO, format=logger_format)
    init_db()
    soul_healer = SoulHealerAppService()
    # =============第一轮对话==============================
    # output = soul_healer.chat_healer("我最近有点不开心，你能帮我吗？")
    # =============第二轮对话==============================
    # response = soul_healer.chat_healer("工作事情太多，干不完")

    messages = soul_healer.pull_messages(pager={'page_size': 10, 'offset': 0})
    print(messages)


    # # tripo_url = soul_healer.create_soul_healer("帮我创建1个心灵治愈师的卡通形象")
    # # soul_healer.export_soul_healer(tripo_url)

    # chat_message_service = ChatMessageService()
    # chat_message_service.save_chat_message('user', "abc")
    # chat_message_service.save_chat_message("assistant", "efg")

    # init_db()
    # session = ChatSession(user_id=0, summary="test", message_time=TimeUtils.system_time_millis())
    # new_session = ChatSession.insert(session)
    # print(new_session)
