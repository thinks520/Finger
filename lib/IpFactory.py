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
        获取域名对应 ip列表、 cname列表、 cdn判断, 内网判断
        """

        host = self.parse_host(url)
        # 获取CNAME
        cname_list = []
        try:
            resolver_cname = dns.resolver.resolve(host, 'CNAME')
            for i in resolver_cname.response.answer:
                for j in i.items:
                    # print(j.to_text())
                    cname_list.append(j.to_text())
        except:
            pass
        cname_list = list(set(cname_list))
        cname = ",".join(cname_list) if cname_list else ""

        # 获取IP
        resolver_ip_list = []
        available_ip_list = []
        ip = ""
        try:
            resolver_ip = dns.resolver.resolve(host, 'A')
            for i in resolver_ip.response.answer:
                for j in i.items:
                    resolver_ip_list.append(j.to_text())
        except:
            pass
        resolver_ip_list = list(set(resolver_ip_list))
        if resolver_ip_list:
            for resolver_ip in resolver_ip_list:
                try:
                    # 校验是否为有效IP
                    ipaddress.ip_address(resolver_ip.strip())
                    available_ip_list.append(resolver_ip)
                except Exception as e:
                    pass
            ip = ",".join(available_ip_list) if available_ip_list else ""
        is_inner = 0
        for available_ip in available_ip_list:
            try:
                if ipaddress.ip_address(available_ip.strip()).is_private:
                    is_inner = 1
            except Exception as e:
                pass
        # 判断CDN
        is_cdn = 0
        if available_ip_list:
            if len(available_ip_list) > 1:
                is_cdn = 1
            else:
                for cdn in self.cdns:
                    if ipaddress.ip_address(available_ip_list[0]) in ipaddress.ip_network(cdn):
                        is_cdn = 1
                        break
        host_data = {"cname": cname, "ip": ip, "is_inner": is_inner, "is_cdn": is_cdn}
        return host_data
