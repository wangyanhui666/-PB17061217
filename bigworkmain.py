#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode

# ----------------------------------
# 汇率调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/80
# ----------------------------------

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from bigwork import Ui_Form


# 定义一些参数用来返回
show = ''
dictforcode = {}
show2 = ''
# 配置您申请的Key
key = '078024c65f4cf520f3fea6bf5427852e'


# 使得业务逻辑分离，调用QTdesigner生成的Ui_Form类作为父类
class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

    # 点击查询按钮1的槽函数：显示人民币对其他币种汇率
    def serch1_clicked(self):
        self.textBrowser1.setPlainText(show)

    # 点击查询按钮2的槽函数.实时汇率查询换算
    def serch2_clicked(self):
        return1 = self.textEdit.toPlainText()
        return2 = self.textEdit_2.toPlainText()
        url = "http://op.juhe.cn/onebox/exchange/currency"
        params = {
            "from": dictforcode[return1],  # 转换汇率前的货币代码
            "to": dictforcode[return2],  # 转换汇率成的货币代码
            "key": key,  # 应用APPKEY(应用详细页查询)
        }
        global show2
        params = urlencode(params)
        f = requests.get(url, params, timeout=10)
        res = f.json()
        print(res)

        # 将得到的数据转换成想要的字符串格式
        show2 = '1 of ' + return1 + '\n' + ' equals to ' + '\n' + res['result'][0]["result"] + ' of ' + return2

        # 判断请求是否成功若成功则显示结果否则显示错误
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                # 成功请求
                print(res["result"])
            else:
                print("%s:%s" % (res["error_code"], res["reason"]))
        else:
            print("request api error")
        self.textBrowser_2.setPlainText(show2)


def main():
    # 1.常用汇率查询
    request1(key)

    # 2.货币列表
    request2(key)

    # 3.GUI界面显示
    a = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    sys.exit(a.exec_())


# 人民币对其他币种汇率查询函数
def request1(appkey):
    url = "http://op.juhe.cn/onebox/exchange/query"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
    }
    params = urlencode(params)
    f = requests.get(url, params, timeout=10)
    global show
    res = f.json()
    dic1 = []

    # 将得到的数据取有用的转换为字典
    for i in range(len(res['result']['list'])):
        float_value = float(res['result']['list'][i][2])
        str_value = str("%.4f" % (10000/float_value))
        dic1.append(res['result']['list'][i][0]+':'+str_value)

    # 重新排版显示为字符串
    for i in range(len(dic1)):
        show = show+dic1[i]+'\n'

    # 判断请求是否成功若成功则显示结果否则显示错误
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(show)
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


#币种及其编码查询函数
def request2(appkey):
    url = "http://op.juhe.cn/onebox/exchange/list"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
    }
    params = urlencode(params)
    f = requests.get(url, params, timeout=10)
    res = f.json()
    # 将返回值转换为需要的字典型
    for i in range(len(res['result']['list'])):
        dictforcode[res['result']['list'][i]['name']] = res['result']['list'][i]['code']

    # 判断请求是否成功若成功则显示结果否则显示错误
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


# 主函数
main()
