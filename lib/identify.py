#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import json
import os
import re
from urllib.parse import urlsplit

from config.color import color
from config.data import logging, Webinfo
from config.data import path
from lib.checkenv import CheckEnv


class Identify:
    def __init__(self):
        self.data = None
        filepath = os.path.join(path.library, 'finger.json')
        if not os.path.exists(filepath):
            CheckEnv.update()
        with open(filepath, 'r', encoding='utf-8') as file:
            finger = json.load(file)
            for name, value in finger.items():
                self.obj = value
            # 初始化指纹库
            self._prepare_app()

    def run(self, data):
        self.data = data
        cms = self._has_app()
        self.data["cms"] = ','.join(set(cms))
        _url = "://{0}".format(urlsplit(self.data['url']).netloc)  # 添加://降低误报率
        _webinfo = str(Webinfo.result)
        if _url in _webinfo and self.data["title"] in _webinfo:
            pass
        else:
            results = {"url": self.data["url"], "cms": self.data["cms"], "title": self.data["title"],
                       "status": self.data["status"], "Server": self.data['Server'],
                       "size": self.data["size"], "is_cdn": self.data["is_cdn"], "ip": self.data["ip"],
                       "is_inner": self.data["is_inner"], "cname": self.data["cname"], "address": self.data["address"],
                       "isp": self.data["isp"]}
            if cms:
                Webinfo.result.insert(0, results)
            else:
                Webinfo.result.append(results)
            Msg = "{0} {1} {2} {4} {3}".format(color.green(self.data['cms']),
                                               color.blue(self.data['Server']), self.data['title'],
                                               color.yellow(self.data['status']), self.data["url"])
            logging.success(Msg)

    def _prepare_app(self):
        for line in self.obj:
            if "regula" == line["method"]:
                self.obj[self.obj.index(line)]["keyword"] = self._prepare_pattern(line["keyword"][0])

    def _prepare_pattern(self, pattern):
        regex, _, rest = pattern.partition('\\;')
        try:
            return re.compile(regex, re.I)
        except re.error as e:
            return re.compile(r'(?!x)x')

    def _has_app(self):
        cms = []
        for line in self.obj:
            flag = 1
            if line['method'] == "faviconhash" and str(self.data["faviconhash"]) == line["keyword"][0]:
                cms.append(line["cms"])
            elif line["method"] == "keyword":
                for key in line["keyword"]:
                    if key not in str(self.data[line["location"]]):
                        flag = 0
                if flag == 1:
                    cms.append(line["cms"])
            elif line["method"] == "regula":
                if line["keyword"].search(self.data[line["location"]]):
                    cms.append(line["cms"])
            else:
                pass
        return cms
