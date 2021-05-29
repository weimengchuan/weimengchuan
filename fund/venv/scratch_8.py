import requests
import time
import execjs
import matplotlib.pyplot as plt
import numpy as np

def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())

    return head + fscode + tail


def getWorth(fscode):
    # 用requests获取到对应的文件
    content = requests.get(getUrl(fscode))

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
    print(name, code)
    return netWorth, ACWorth


netWorth, ACWorth = getWorth('002770')
print(netWorth)


L_all = np.array(netWorth)

#plt.plot(L)
#plt.show()

#plt.plot(L[:100][::-1])
#plt.show()

day = 100  #最近的天数
capital = 100 #本金
ratio = 0.05 #每天增减钱的比例



def fixed_ratio_turnover(capital, L_all, ratio, day):
    L = L_all[0 : day]
    K = np.zeros((len(L) ))
    for i in range(len(L) - 1):
        i_day = len(L) - i - 1
        K[i] = (L[i_day - 1] - L[i_day])/L[i_day] #每一天的增长率
    
    #plt.plot(K[len(L)-60:-1])
    #plt.show()
    
    a = np.array([int(i) for i in (K > 0)]) * 2 - 1 #每一天的增长率正负
    
    K_day_stay = (K[len(L)-60:-1] + 1).prod()
    
    K_day = np.zeros((len(L))) #基金账户里的钱
    turnover = np.zeros((len(L))) #上一天三点前增减的钱
    K_day_real = np.zeros((len(L))) #实际的钱
    
    K_day[0] = capital
    turnover[0] = 0 #上一天三点前增减的钱
    K_day_real[0] = capital
    for i in range(len(L) - 1):
        turnover[i + 1] = a[i]*K_day[i]*ratio
        K_day[i + 1] = (K_day[i] - turnover[i + 1]) * (K[i] + 1)
        K_day_real[i + 1] = K_day[i + 1] + turnover[0 : i + 2].sum()
    return [K_day_real, K_day, turnover]

[K_day_real, K_day, turnover] = fixed_ratio_turnover(capital, L_all, ratio, day)

plt.plot(K_day_real) #画出每天交易结束后投资钱的总额
plt.show()
plt.figure(figsize=(10,5))
plt.plot(netWorth[:day][::-1]) #画出每天交易结束后净值
plt.show()


ratio_all = np.arange(-0.3,0,0.01)
K_day_real_bt_ratio = np.zeros((len(ratio_all)))
for i in range(len(ratio_all)):
    ratio = ratio_all[i]
    [K_day_real, K_day, turnover] = fixed_ratio_turnover(capital, L_all, ratio, day)
    K_day_real_bt_ratio[i] = K_day_real[-1]
plt.xticks(np.arange(len(ratio_all)), (ratio_all*100).astype(int))
plt.plot(K_day_real_bt_ratio) #画出每天交易结束后投资钱的总额
plt.show()