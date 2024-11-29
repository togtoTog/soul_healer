# -*- coding: UTF-8 -*-

class ChatMessageView:

    def __init__(self, message):
        self.message_id = message.id
        self.content = message.content.decode('utf-8')
        self.session_id = message.session_id
        self.from_role = message.from_role
        self.message_time = message.message_time