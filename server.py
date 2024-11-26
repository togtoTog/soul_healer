import logging

from app.SoulHealerAppService import SoulHealerAppService

logger_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(message)s'
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=logger_format)

    # chat = KwaiYiiChatService()
    # # =============第二轮对话==============================
    # msg1 = chat.get_chat_message("user", "a=1，b=3, a+b=多少")
    # output = chat.do_chat_messages([msg1])
    # print(output)
    # # =============第二轮对话==============================
    # msg_assistant = chat.get_chat_message("assistant", output)
    # msg_user = chat.get_chat_message("user", "c=3，b+c=多少")
    # response = chat.do_chat_messages([msg1, msg_assistant, msg_user])
    # print(response)

    soul_healer = SoulHealerAppService()
    tripo_url = soul_healer.create_soul_healer("帮我创建1个心灵治愈师的卡通形象")
    soul_healer.export_soul_healer(tripo_url)

