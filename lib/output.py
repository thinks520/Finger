#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import os
import time
import json
import base64
import xlsxwriter
from config.data import path, Webinfo, Save, UrlError
from config.data import logging


class Output:
    def __init__(self):
        self.nowTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        Webinfo.result = Webinfo.result + UrlError.result
        self.filename_json = Save.output_file
        self.filename_xls = Save.output_file
        self.path_json = os.path.join(path.output, self.filename_json)
        self.path_xls = os.path.join(path.output, self.filename_xls)
        if Save.output_file.endswith('.json') and Webinfo.result:
            self.outJson()
        if Save.output_file.endswith('.xlsx') and Webinfo.result:
            self.outXls()

    def outJson(self):
        with open(self.path_json, 'w') as file:
            file.write(json.dumps(Webinfo.result))
        print()
        successMsg = "结果文件输出路径为:{0}".format(self.path_json)
        logging.success(successMsg)

    def outXls(self):
        with xlsxwriter.Workbook(self.path_xls) as workbook:
            worksheet = workbook.add_worksheet('Finger scan')
            bold = workbook.add_format({"bold": True, "valign": "center"})
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 40)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 15)
            worksheet.set_column('F:F', 15)
            worksheet.set_column('G:G', 30)
            worksheet.set_column('H:H', 10)
            worksheet.set_column('I:I', 30)
            worksheet.set_column('J:J', 30)
            worksheet.write('A1', 'Url', bold)
            worksheet.write('B1', 'Title', bold)
            worksheet.write('C1', 'cms', bold)
            worksheet.write('D1', 'Server', bold)
            worksheet.write('E1', 'status', bold)
            worksheet.write('F1', 'size', bold)
            worksheet.write('G1', 'ip', bold)
            worksheet.write('H1', 'cname', bold)
            worksheet.write('I1', 'is_cdn', bold)
            worksheet.write('J1', 'is_inner', bold)
            worksheet.write('K1', 'address', bold)
            worksheet.write('L1', 'isp', bold)
            row = 1
            col = 0
            for value in Webinfo.result:
                worksheet.write(row, col, value["url"])
                worksheet.write(row, col + 1, value["title"])
                worksheet.write(row, col + 2, value["cms"])
                worksheet.write(row, col + 3, value["Server"])
                worksheet.write(row, col + 4, value["status"])
                worksheet.write(row, col + 5, value["size"])
                worksheet.write(row, col + 6, value["ip"])
                worksheet.write(row, col + 7, value["cname"])
                worksheet.write(row, col + 8, value["is_cdn"])
                worksheet.write(row, col + 9, value["is_inner"])
                worksheet.write(row, col + 10, value["address"])
                worksheet.write(row, col + 11, value["isp"])
                row = row + 1

        print()
        successMsg = "结果文件输出路径为:{0}".format(self.path_xls)
        logging.success(successMsg)
