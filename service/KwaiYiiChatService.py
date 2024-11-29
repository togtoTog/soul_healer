import copy
import logging

from kess.framework import ClientOption, GrpcClient

import protos.maas_chat_gateway_pb2 as maas_chat_gateway_pb2
from exception.ApiCodeEnum import ApiCodeEnum
from exception.ApiException import ApiException
from protos.maas_chat_gateway_pb2_grpc import MaaSChatGatewayServiceStub

grpc_service_name = "mmu-maas-chat-gateway-service"

client_option = ClientOption(
    biz_def='infra',
    grpc_service_name=grpc_service_name,
    grpc_stub_class=MaaSChatGatewayServiceStub,
)
client = GrpcClient(client_option)

logger = logging.getLogger(__name__)


# KwaiYii聊天对接


class KwaiYiiChatService:

    # 初始化
    def __init__(self):
        self.stub = client.get_stub()
        # 默认的请求参数
        req = maas_chat_gateway_pb2.KuaiYiChatCompletionRequest()
        req.key = "065731591f1e40e99f016bd03c2ca500"
        req.end_point = "admin_KwaiYii-v1-66B_base"
        req.n = 1
        self.req = req

    # 构建聊天消息体
    def get_chat_message(self, role, content):
        msg = maas_chat_gateway_pb2.MessageInfo()
        msg.role = role
        msg.content_str = content
        logger.info("对话消息 %s %s", role, content)
        return msg

    # 非流式对话
    def do_chat_messages(self, chat_config, messages=None, timeout=60000):
        if messages is None or len(messages) <= 0:
            messages = []
        try:
            # 使用拷贝对象
            req = copy.deepcopy(self.req)
            # 最开始插入背景提示词
            theme = chat_config['theme']
            if theme is not None and theme != '':
                theme_message = self.get_chat_message('system', theme)
                req.messages.append(theme_message)
            for message in messages:
                from_role = int(message.from_role)
                decode_message = message.content.decode('utf-8')
                if from_role == 1:
                    chat_message = self.get_chat_message(role='user', content=decode_message)
                    req.messages.append(chat_message)
                elif from_role == 2:
                    chat_message = self.get_chat_message(role='assistant', content=decode_message)
                    req.messages.append(chat_message)
                else:
                    raise ApiException(ApiCodeEnum.CHAT_MESSAGE_ROLE_ERROR, "the message role is error!")
            req.time_out_ms = timeout
            # req.random_seed = random.randint(0, 200)
            response = self.stub.Chat(req)
            resp_status = response.status
            logger.info("[KwaiYii] chat message success! code = %s, message = %s, ", resp_status.code, resp_status.msg)
            output = ""
            if len(response.choices) > 0:
                output = response.choices[0].message["assistant"]
            return output
        except Exception as e:
            logger.error("[KwaiYii] chat message error!", exc_info=True)
            raise ApiException(ApiCodeEnum.CHAT_MESSAGE_SERVICE_ERROR, "[KwaiYii] chat message error!")
