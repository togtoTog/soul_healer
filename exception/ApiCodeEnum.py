from enum import Enum,unique

@unique
class ApiCodeEnum(Enum):
    SUCCESS = 1,
    TEXT_TO_IMAGE_ERROR = 2,
    GET_TEXT_IMAGE_ERROR = 3,
    IMAGE_TO_TRIPO_ERROR = 4,
    GET_TRIPO_FILE_ERROR = 5,
    CHAT_MESSAGE_ROLE_ERROR = 6,
    CHAT_MESSAGE_SERVICE_ERROR = 7