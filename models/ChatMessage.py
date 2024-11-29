import json

from objtyping import to_primitive
from sqlalchemy import ForeignKey, Column, Integer, String, UnicodeText

from database import Base, db_session


class ChatMessage(Base):
    __tablename__ = "chat_message"
    id = Column(Integer, primary_key=True)
    # 用户ID
    user_id = Column(String(128))
    # 所属的会话ID
    session_id = Column(Integer, ForeignKey("chat_session.id"))
    # 用户角色 system:0, user:1, assistant: 2
    from_role = Column(Integer)
    # 消息内容
    content = Column(UnicodeText)
    # 消息时间
    message_time = Column(Integer)

    def __init__(self, user_id=0, session_id=None, from_role=None, content=None, message_time=0):
        super().__init__()
        self.user_id = user_id
        self.session_id = session_id
        self.from_role = from_role
        self.content = content.encode(encoding="utf-8")
        self.message_time = message_time

    @classmethod
    def insert(cls, message):
        db_session.add(message)
        db_session.commit()
        return message

    @classmethod
    def pull_chat_messages(cls, user_id=0, page_offset=0, page_size=10):
        messages = (
            db_session.query(ChatMessage)
            .filter(ChatMessage.user_id == str(user_id))
            .order_by(ChatMessage.id.desc())
            .offset(page_offset)
            .limit(page_size)
            .all()
        )
        if messages is None:
            return []
        return sorted(messages, key=lambda x: x.id, reverse=False)

    def __repr__(self):
        return json.dumps(to_primitive(self))
