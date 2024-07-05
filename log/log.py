import inspect
import logging
from pathlib import Path
from typing import Dict, Any
from logging.handlers import RotatingFileHandler

from config.config import Config
from .log_formatter import LogFormatter


# noinspection SpellCheckingInspection
class LoggerManager:
    """
    日志管理器类，负责设置和管理日志记录器

    Attributes:
    - __loggers (Dict[str, Any]): 存储已创建的日志记录器
    - __default_log_file (str): 默认的日志文件名
    """

    __loggers: Dict[str, Any] = {}
    __default_log_file = "stream.log"

    @staticmethod
    def __setup_logger(log_file: str):
        """
        设置日志记录器

        Parameters:
        - log_file (str): 日志文件名

        Returns:
        - logging.Logger: 设置好的日志记录器
        """
        log_file_path = Path(Config().log_path) / log_file
        if not log_file_path.parent.exists():
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

        __logger = logging.getLogger(log_file_path.stem)
        __logger.setLevel(logging.DEBUG)

        for handler in __logger.handlers:
            __logger.removeHandler(handler)

        # 终端日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = LogFormatter(f"%(level_text)s%(message)s")
        console_handler.setFormatter(console_formatter)
        __logger.addHandler(console_handler)

        # 文件日志
        file_handler = RotatingFileHandler(filename=log_file_path,
                                           mode='w',
                                           maxBytes=50 * 1024 * 1024,
                                           backupCount=3,
                                           encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = LogFormatter(f"【%(levelname)s】%(asctime)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        __logger.addHandler(file_handler)

        return __logger

    def logger(self, method: str, msg: str, *args, **kwargs):
        """
        记录日志

        Parameters:
        - method (str): 日志记录方法（例如：info、debug、warning、error、critical）
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        caller_name = self.__get_caller()
        logfile = self.__default_log_file

        __logger = self.__loggers.get(logfile)
        if not __logger:
            __logger = self.__setup_logger(logfile)
            self.__loggers[logfile] = __logger

        if hasattr(__logger, method):
            method = getattr(__logger, method)
            method(f"{caller_name} - {msg}", *args, **kwargs)

    @staticmethod
    def __get_caller():
        """
        获取调用者的文件名称

        Returns:
        - str: 调用者所在的文件名称
        """
        caller_name = None
        for stack in inspect.stack()[2:]:
            filepath = Path(stack.filename)
            parts = filepath.parts
            caller_name = parts[-2] if parts[-1] == "__init__.py" else parts[-1]
            if caller_name == "log.py":
                continue
            if caller_name and isinstance(caller_name, str):
                break
            if not caller_name and len(parts) != 1:
                break
        return caller_name or "log.py"

    def info(self, msg: str, *args, **kwargs):
        """
        记录 INFO 级别的日志

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("info", msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        """
        记录 DEBUG 级别的日志

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("debug", msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """
        记录 WARNING 级别的日志

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("warning", msg, *args, **kwargs)

    def warn(self, msg: str, *args, **kwargs):
        """
        记录 WARNING 级别的日志（别名）

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("warning", msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """
        记录 ERROR 级别的日志

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("error", msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """
        记录 CRITICAL 级别的日志

        Parameters:
        - msg (str): 日志消息
        - args: 可变参数
        - kwargs: 关键字参数
        """
        self.logger("critical", msg, *args, **kwargs)


# 初始化公共日志
logger = LoggerManager()
