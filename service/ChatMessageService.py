import logging
import time

from models.ChatMessage import ChatMessage
from models.ChatSession import ChatSession
from utils.TimeUtils import TimeUtils

logger = logging.getLogger(__name__)

split_char = '|'

session_config = {
    # "interval_time": 3 * 60 * 60 * 1000
    "interval_time": 1 * 60 * 1000
}


class ChatMessageService:

    # 根据用户ID，获取最新的会话信息
    @staticmethod
    def build_chat_session(user_id=0, message_time=0):
        session = ChatSession.last_session(user_id)
        interval_time = session_config['interval_time']
        current_time = int(round(time.time() * 1000))
        # 会话不存在或者会话已过期，则新建会话
        if session is None:
            session = ChatSession(user_id=user_id, summary='', message_time=message_time)
            ChatSession.insert(session)
        elif current_time - session.update_time > interval_time:
            ChatSession.close(session)
            session = ChatSession(user_id=user_id, summary='', message_time=message_time)
            ChatSession.insert(session)
        return session

    # 保存聊天记录
    @staticmethod
    def save_chat_message(from_role, content):
        if content is None or content == '':
            return None, None
        ts = TimeUtils.system_time_millis()
        session = ChatMessageService.build_chat_session(message_time=ts)
        message = ChatMessage(session_id=session.id, from_role=from_role, content=content, message_time=ts)
        new_message = ChatMessage.insert(message)
        return session, new_message

    @staticmethod
    def pull_chat_messages(user_id=0, pager=None):
        page_size = pager['page_size']
        page_offset = pager['offset']
        return ChatMessage.pull_chat_messages(user_id=user_id, page_offset=page_offset, page_size=page_size)
