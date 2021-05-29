#-*-coding:utf-8-*-
import requests
import time
import execjs
import json
import numpy as np
import matplotlib.pyplot as plt
import os

def getUrl(fundCode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())

    return head + fundCode + tail


def getWorth(fundCode):
    # 用requests获取到对应的文件
    content = requests.get(getUrl(fundCode))

    # 使用execjs获取到相应的数据
    jsContent = execjs.compile(content.text)
    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    # 单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    # 累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')

    netWorth = []
    ACWorth = []

    # 提取出里面的净值
    for dayWorth in netWorthTrend[::-1]:
        netWorth.append(dayWorth['y'])

    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])

    fundInfo = dict()
    fundInfo['fundName'] = name
    fundInfo['fundCode'] = code
    fundInfo['updateDate'] = time.localtime()

    fundData = dict()
    fundData['dayK'] = netWorth
    fundInfo['fundData'] = fundData

    curPath = os.getcwd()
    fundDataPath = curPath.replace('\\venv', '') + '\\data\\'
    fundDataName = name + '_' + code + '.json'
    with open(fundDataPath + fundDataName, 'w', encoding='utf-8') as f:
        json.dump(fundInfo, f)
    print('正在获取 : ' + name + '(' + code + ')')
    return netWorth, ACWorth, name



