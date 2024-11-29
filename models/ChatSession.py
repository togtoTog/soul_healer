import json
import time
from enum import Enum, unique

from objtyping import to_primitive
from sqlalchemy import Column, Integer, String

from database import Base, db_session
from utils.TimeUtils import TimeUtils


@unique
class SessionStatus(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSE = 1000

class ChatSession(Base):
    __tablename__ = "chat_session"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(128))
    # 会话状态 0未知 1开启 1000关闭
    status = Column(Integer)
    # 会话摘要
    summary = Column(String(1024), nullable=True)
    min_message_time = Column(Integer)
    max_message_time = Column(Integer)
    create_time = Column(Integer)
    update_time = Column(Integer)

    def __init__(self, user_id=None, summary=None, message_time=None):
        super().__init__()
        self.user_id = user_id
        self.status = SessionStatus.OPEN.value
        self.summary = summary
        self.min_message_time = message_time
        self.max_message_time = message_time
        ts = TimeUtils.system_time_millis()
        self.create_time = ts
        self.update_time = ts

    @classmethod
    def insert(cls, session):
        db_session.add(session)
        db_session.commit()
        return session

    @classmethod
    def update(cls, session_id, new_session):
        if session_id is None or new_session is None:
            return None
        old_session = cls.get(session_id)
        if old_session:
            if new_session.status is not None:
                old_session.status = new_session.status
            if new_session.summary is not None:
                old_session.summary = new_session.summary
            if new_session.max_message_time is not None:
                old_session.max_message_time = new_session.max_message_time
            old_session.update_time = TimeUtils.system_time_millis()
            db_session.commit()

    @classmethod
    def close(cls, session):
        if session is None:
            return
        session.status = SessionStatus.CLOSE.value
        session.update_time = TimeUtils.system_time_millis()
        db_session.commit()

    @classmethod
    def delete(cls, session_id):
        session = cls.get(session_id)
        if session:
            db_session.delete(session)
            db_session.commit()
            return True
        else:
            return False

    @classmethod
    def get(cls, session_id):
        return (
            db_session.query(ChatSession)
            .filter_by(id=session_id)
            .first()
        )

    @classmethod
    def last_session(cls, user_id):
        session = (
            db_session.query(ChatSession)
            .filter(ChatSession.user_id == str(user_id))
            .order_by(ChatSession.id.desc())
            .first()
        )
        return session

    def __repr__(self):
        return json.dumps(to_primitive(self))
