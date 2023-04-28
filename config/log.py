#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import logging
import sys
from config.color import color
from colorama import init as wininit

wininit(autoreset=True)


# 设置日志等级
class LoggingLevel:
    def __init__(self):
        pass

    SUCCESS = 9
    SYSINFO = 8
    ERROR = 7
    WARNING = 6


logging.addLevelName(LoggingLevel.SUCCESS, color.cyan("[+]"))
logging.addLevelName(LoggingLevel.SYSINFO, color.green("[INFO]"))
logging.addLevelName(LoggingLevel.ERROR, color.red("[ERROR]"))
logging.addLevelName(LoggingLevel.WARNING, color.yellow("[WARNING]"))

# 初始化日志
LOGGER = logging.getLogger('Finger')
# 设置输出格式
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    datefmt=color.fuchsia("[%H:%M:%S]")
)
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(formatter)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(LoggingLevel.WARNING)


class MyLogger:

    def __init__(self):
        pass

    @staticmethod
    def info(msg):
        return LOGGER.log(LoggingLevel.SYSINFO, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(LoggingLevel.ERROR, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(LoggingLevel.WARNING, msg)

    @staticmethod
    def success(msg):
        return LOGGER.log(LoggingLevel.SUCCESS, msg)
