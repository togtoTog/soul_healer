import traceback
import copy

from kess.framework import ClientOption, GrpcClient

import protos.maas_chat_gateway_pb2 as maas_chat_gateway_pb2
from protos.maas_chat_gateway_pb2_grpc import MaaSChatGatewayServiceStub

grpc_service_name = "mmu-maas-chat-gateway-service"

client_option = ClientOption(
    biz_def='infra',
    grpc_service_name=grpc_service_name,
    grpc_stub_class=MaaSChatGatewayServiceStub,
)
client = GrpcClient(client_option)


# KwaiYii聊天对接


class KwaiYiiChatService:

    # 初始化
    def __init__(self):
        self.stub = client.get_stub()
        # 默认的请求参数
        req = maas_chat_gateway_pb2.KuaiYiChatCompletionRequest()
        req.key = "065731591f1e40e99f016bd03c2ca500"
        req.end_point = "admin_KwaiYii-v1-66B_base"
        self.req = req

    # 构建聊天消息体
    def get_chat_message(self, role, content):
        msg = maas_chat_gateway_pb2.MessageInfo()
        msg.role = role
        msg.content_str = content
        return msg

    # 非流式对话
    def do_chat_messages(self, messages=None, timeout=60000):
        if messages is None:
            messages = []
        try:
            req = copy.deepcopy(self.req)
            for message in messages:
                req.messages.append(message)
            req.time_out_ms = timeout
            response = self.stub.Chat(req)
            output = ""
            if len(response.choices) > 0:
                output = response.choices[0].message["assistant"]
            return output
        except Exception as e:
            traceback.print_exc()
