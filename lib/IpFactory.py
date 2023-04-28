#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import ipaddress
import json
import os
import re
import socket
import dns.resolver
from urllib.parse import urlsplit

from config.data import path
from lib.ip2Region import Ip2Region


class IPFactory:
    def __init__(self):
        cdnFile = os.path.join(path.library, 'cdn_ip_cidr.json')
        dbFile = os.path.join(path.library, "data", "ip2region.db")
        self.searcher = Ip2Region(dbFile)
        with open(cdnFile, 'r', encoding='utf-8') as file:
            self.cdns = json.load(file)

    def parse_host(self, url):
        host = urlsplit(url).netloc
        if ':' in host:
            host = re.sub(r':\d+', '', host)
        return host

    def factory(self, url):
        """
        获取域名对应 ip列表、 cname列表、 cdn判断
        """

        host = self.parse_host(url)
        # 获取CNAME
        cname_list = []
        try:
            CNAME = dns.resolver.resolve(host, 'CNAME')
            for i in CNAME.response.answer:
                for j in i.items:
                    # print(j.to_text())
                    cname_list.append(j.to_text())
        except:
            pass
        cname_list = list(set(cname_list))
        cname = ",".join(cname_list) if cname_list else ""

        # 获取IP
        ip_list = []
        try:
            IP = dns.resolver.resolve(host, 'A')
            for i in IP.response.answer:
                for j in i.items:
                    # print(j.to_text())
                    ip_list.append(j.to_text())
        except:
            pass
        ip_list = list(set(ip_list))
        ip = ",".join(ip_list) if ip_list else ""

        # 判断CDN
        is_cdn = 0
        if len(ip_list) > 1:
            is_cdn = 1
        else:
            for cdn in self.cdns:
                if ipaddress.ip_address(ip_list[0]) in ipaddress.ip_network(cdn):
                    is_cdn = 1
                    break
        return cname, ip, is_cdn

