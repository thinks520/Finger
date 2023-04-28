#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
from colorama import init as win_init

from lib.checkenv import CheckEnv
from lib.cmdline import cmdline
from lib.ipAttributable import IpAttributable
from lib.options import InitOptions
from lib.output import Output
from lib.req import Request

win_init(autoreset=True)

if __name__ == '__main__':
    # 打印logo
    # print(config.Banner)
    # 检测环境
    check = CheckEnv()
    # 加载参数
    options = InitOptions(cmdline())
    run = Request()
    IpAttributable()
    save = Output()
