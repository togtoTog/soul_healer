import time


class TimeUtils:

    @staticmethod
    def system_time_millis():
        return int(round(time.time() * 1000))


    @staticmethod
    def system_time_seconds():
        return int(time.time())