#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import hashlib
import os
import sys
import time

import requests

from config.config import head, FingerPrintUpdate
from config.data import path, logging


class CheckEnv:
    def __init__(self):
        self.py_version = sys.version_info
        self.path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_check()
        if FingerPrintUpdate:
            self.update()

    def python_check(self):
        if self.py_version < (3, 7):
            logging.error(f"此Python版本 ('{self.py_version}') 不兼容,成功运行程序你必须使用版本 >= 3.6 (访问 ‘https://www.python.org/downloads/")

    def path_check(self):
        try:
            os.path.isdir(self.path)
        except UnicodeEncodeError:
            errMsg = "your system does not properly handle non-ASCII paths. "
            errMsg += "Please move the project root directory to another location"
            logging.error(errMsg)
            exit(0)
        path.home = self.path
        path.output = os.path.join(self.path, 'output')
        path.config = os.path.join(self.path, 'config')
        path.library = os.path.join(self.path, 'library')
        if not os.path.exists(path.output):
            warnMsg = "The output folder is not created, it will be created automatically"
            logging.warning(warnMsg)
            os.mkdir(path.output)

    @staticmethod
    def update():
        try:
            is_update = True
            nowTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            logging.info("正在在线更新指纹库。。")
            Fingerprint_Page = "https://cdn.jsdelivr.net/gh/EASY233/Finger/library/finger.json"
            response = requests.get(Fingerprint_Page, timeout=10, headers=head)
            filepath = os.path.join(path.library, "finger.json")
            if not os.path.exists(filepath):
                with open(filepath, "wb") as file:
                    file.write(response.content)
            bak_file_path = os.path.join(path.library, "finger_{}.json.bak".format(nowTime))
            with open(filepath, "rb") as file:
                if hashlib.md5(file.read()).hexdigest() == hashlib.md5(response.content).hexdigest():
                    logging.info("指纹库已经是最新")
                    is_update = False
            if is_update:
                logging.info("检查到指纹库有更新,正在同步指纹库。。。")
                os.rename(filepath, bak_file_path)
                with open(filepath, "wb") as file:
                    file.write(response.content)
                with open(filepath, 'rb') as file:
                    Msg = "更新成功！" if hashlib.md5(file.read()).hexdigest() == hashlib.md5(
                        response.content).hexdigest() else "更新失败"
                    logging.info(Msg)
        except Exception as e:
            logging.warning("在线更新指纹库失败！")
