import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from simple_settings import settings


class Logger(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._logger = Logger.logger_init()
        return cls._instance

    @staticmethod
    def logger_init():
        handler = TimedRotatingFileHandler(settings.LOG_PATH,
                                           when="w0",
                                           interval=1,
                                           backupCount=5)

        formatter = logging.Formatter(settings.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        streamHandler = StreamHandler()
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)
        return logger

    def get_logger(self):
        return self._logger
