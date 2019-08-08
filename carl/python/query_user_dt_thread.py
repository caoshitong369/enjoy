# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "/data/python/Admin")))
import grpc
from pb.usercenter.user import service_pb2, service_pb2_grpc
from pb.coin import query_pb2_grpc, apis_pb2
from threading import Thread
from utils.email_ import send_dt
import re
import logging
import time
from datetime import datetime
import xlwt
import xlrd
from apscheduler.schedulers.blocking import BlockingScheduler
from configs.site_settings import COIN_QUERY_GRPC_ADDR, USERCENTER_GRPC_ADDR, GLOVAL_USER_EMAIL_LIST, GLOBAL_USER_LIST

global_excel_data = {}
global_excel_header = []
global_excel_end = []
global_total = 0


def make_time():
    format_time = datetime.now().strftime("%m-%d")
    return format_time


# 根据uid查找用户id指定货币的余额，默认货币是DT
def query_user_dt(user_id, coin_id=104):
    coin_query_rpc_conn = grpc.insecure_channel(COIN_QUERY_GRPC_ADDR)
    coin_query_rpc_client = query_pb2_grpc.CoinQueryServiceStub(channel=coin_query_rpc_conn)
    req = apis_pb2.UserCoinDetailRequest(uid=apis_pb2.CoinUserIDRequest(user_id=user_id), coin_id=coin_id)
    rpc = coin_query_rpc_client.UserCoinDetail(req, metadata=[("app_id", "admin")])
    global global_total
    if rpc.base_reply.code == 1:
        user_id = int(rpc.user_id)
        amount = round(float(rpc.quantity), 2)
        if user_id in global_excel_data:
            global_excel_data[user_id].append(amount)
        else:
            num = len(global_excel_header)
            global_excel_data[user_id] = [user_id]
            for i in range(num - 2):
                global_excel_data[user_id] += [""]
            global_excel_data[user_id].append(amount)
        global_total += amount

    return


global_list = set()
excel_list_uid = set()


# 根据指定的uid查找他邀请的人的id
def query_user_dts(uid):
    usercenter_rpc_conn = grpc.insecure_channel(USERCENTER_GRPC_ADDR)
    usercenter_rpc_client = service_pb2_grpc.UserServiceStub(channel=usercenter_rpc_conn)
    list1 = []
    req = service_pb2.ListUserInvitedRequest(uid=uid)
    rpc = usercenter_rpc_client.ListUserInvited(req, metadata=[("app_id", "admin")])
    if rpc.baseReply.code == 1:
        data = rpc.invite_infos
        if data:
            for res in data:
                if int(res.uid) not in global_list:
                    list1.append(int(res.uid))
            mul_threading_produce(list1)
    return


# 查找邀请人的id
def mul_threading_produce(uid_list):
    threads = []
    nloops = range(len(uid_list))
    if len(uid_list) > 0:
        for uid in uid_list:
            global_list.add(uid)
            t = Thread(target=query_user_dts, args=(uid,))
            threads.append(t)
        for loop in nloops:
            threads[loop].start()
        for loop in nloops:
            threads[loop].join()
    return


# 用线程根据id查找用户货币的余额
def mul_threading_consumer(uid_lists):
    threads = []
    nloops = range(len(uid_lists))
    if len(uid_lists) > 0:
        for uid in uid_lists:
            t = Thread(target=query_user_dt, args=(uid,))
            threads.append(t)
    for nloop in nloops:
        threads[nloop].start()
    for nloop in nloops:
        threads[nloop].join()
    return


def read_excel():
    global global_excel_header
    global global_excel_data
    global global_excel_end
    data = xlrd.open_workbook("DT余额.xls")
    table = data.sheet_by_index(0)
    num_rows = table.nrows
    for num in range(num_rows):
        if num == 0:
            global_excel_header = table.row_values(num, start_colx=0, end_colx=None)
        if num == num_rows - 1:
            global_excel_end = table.row_values(num, start_colx=0, end_colx=None)
        if num_rows - 1 > num > 0:
            excel_list = table.row_values(num, start_colx=0, end_colx=None)
            global_excel_data[excel_list[0]] = excel_list
            excel_list_uid.add(excel_list[0])


class write_excel(object):

    def __init__(self, data):
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.worksheet = self.workbook.add_sheet("DT余额")
        self.excel_data = data
        self.count = 1
        self.fname = "DT余额.xls"

    def write_excel_title(self, header):
        for i in range(0, len(header)):
            col = self.worksheet.col(i)
            col.width = 256 * 18
            if i == (len(header) - 1):
                self.worksheet.col(i).width = 256 * 23
            self.worksheet.write(0, i, header[i], xlwt.easyxf(
                'font:height 200, name Arial_Unicode_MS, colour_index black, bold on;align: horiz center;'))

    def rows_write(self):
        default = xlwt.easyxf("align: horiz center;")
        for data_list in self.excel_data.values():
            for num, rows in enumerate(data_list):
                self.worksheet.write(self.count, num, rows, default)
            self.count += 1
        for numb, row in enumerate(global_excel_end):
            self.worksheet.write(self.count, numb, row, default)

    def __enter__(self):
        self.write_excel_title(global_excel_header)
        self.rows_write()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.workbook.save(self.fname)
        pass


TABLE = """  <table border="1">
                <thead>
                <tr class="text-c">
                    {}
                </tr>
                </thead>
                <tbody>
                {}
                </tbody>
            </table>
"""
table_header_parts = """<tr class="text-c">
                   {}
                </tr>
"""
table_part = """<tr class="text-c">
                   {}
                </tr>
    """


# 发送邮件
def send_email(receiver_list):
    receivers = []
    if len(receiver_list) > 0:
        for recv in receiver_list:
            if re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$", recv):
                receivers.append(recv)
            else:
                logging.debug("错误的邮箱地址：email_receivers:{}".format(recv))
    title = "统计DT余额"
    table_content = ""
    table_end = ""
    table_head_part = ""
    num = 1
    for value in global_excel_data.values():
        table_body_part = ""
        table_body_part += "<td>{}</td>".format(num) + "\n"
        for data in value:
            table_body_part += "<td>{}</td>".format(data) + "\n"
        num += 1
        table_content += table_part.format(table_body_part) + "\n"
    table_end += "<td>{}</td>".format(num) + "\n"
    for end in global_excel_end:
        table_end += "<td>{}</td>".format(end) + "\n"
    table_content += table_part.format(table_end)
    table_head_part += "<th>{}</th>".format("Serial number") + "\n"
    for head in global_excel_header:
        table_head_part += "<th>{}</th>".format(head) + "\n"
    table_head_content = table_header_parts.format(table_head_part)
    text_cn = TABLE.format(table_head_content, table_content)
    format_time = make_time()
    email_time_cn = format_time
    send_ = Thread(target=send_dt, args=(title, text_cn, email_time_cn, receivers))
    send_.start()
    send_.join()


# 判断文件是否存在的逻辑
def exists_file(user_id_list):
    global global_excel_header
    global global_excel_end
    date_time = make_time()
    title = "{} Balance".format(date_time)
    if os.path.exists("DT余额.xls"):
        read_excel()
        if title in global_excel_header:
            user_id_list = user_id_list - excel_list_uid
            mul_threading_consumer(user_id_list)
            total = sum(global_excel_end[1:]) + global_total
            global_excel_end[-1:] = (total,)
        else:
            global_excel_header.append(title)
            mul_threading_consumer(user_id_list)
            global_excel_end.append(global_total)
    else:
        global_excel_header = ["user_id", title]
        mul_threading_consumer(user_id_list)
        global_excel_end = ["total", global_total]


# 脚本主程序
def main():
    # 初始化全局变量
    global global_excel_data, global_total, global_excel_header, global_excel_end, global_list
    global_excel_data = {}
    global_excel_header = []
    global_excel_end = []
    global_total = 0
    global_list = set()
    t = Thread(target=mul_threading_produce, args=(GLOBAL_USER_LIST,))
    t.start()
    t.join()
    exists_file(global_list)
    with write_excel(global_excel_data):
        print "开始写入"
    receiver_list = GLOVAL_USER_EMAIL_LIST
    send_email(receiver_list)


if __name__ == '__main__':
    # 定时任务
    sched = BlockingScheduler()
    sched.add_job(main, 'interval', days=1, max_instances=5, next_run_time=datetime.now())
    sched.start()
