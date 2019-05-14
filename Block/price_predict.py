import requests
import numpy as np
from model import data_nornalization
from model import predict
import copy
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

import tkinter as tk
ave_price, origin_price_data, predicted_price = 0,0,0
ave_price_show = None
origin_price_data_show = None
predicted_price_show = None
imgLabel = None
def load_btc_data(url, data):
    # 获取最新80笔交易的数据
    r = requests.get(url)
    content = r.json()
    datas = content['data']
    for d in datas:
        data.append([d['type'], float(d['rate']), float(d['amount']), float(d['total'])])

def data_process(data):
    # 对数据进行处理
    for d in data:
        if d[0] == 'buy':
            d[0] = 1
        else:
            d[0] = 0

def price_predict():

    url = 'https://data.gateio.co/api2/1/tradeHistory/btc_usdt'
    data = []
    load_btc_data(url, data)
    data_process(data)

    origin_price_data = copy.deepcopy(np.array(data).T[1])

    #对数据归一化
    new_btc_data, max, min = data_nornalization(data)

    new_btc_data = np.array(new_btc_data).reshape((1,80,4))

    ave_price = origin_price_data.mean()
    # 预测价格
    result = predict(new_btc_data)
    predicted_price = result[0][0] *(max[1]-min[1]) + min[1]

    global ave_price_show, origin_price_data_show, predicted_price_show, image_name, imgLabel
    ave_price_show = tk.StringVar()
    origin_price_data_show = tk.StringVar()
    predicted_price_show = tk.StringVar()
    ave_price_show.set('最新80笔交易的平均价格:'+str(ave_price))
    origin_price_data_show.set('当前最新价格:' + str(origin_price_data[-1]))
    predicted_price_show.set('预测的下一次交易的价格:' + str(predicted_price))

    print('最新80笔交易的平均价格:{}'.format(ave_price))
    print('当前最新价格：{}'.format(origin_price_data[-1]))
    print('预测的下一次交易的价格:{}'.format(predicted_price))

    #可视化
    l1 = range(1, len(origin_price_data)+1)
    plt.plot(l1, origin_price_data, 'b-', color='blue')
    l2 = [80, 81]
    predict_data = [origin_price_data[-1], predicted_price]
    plt.plot(l2, predict_data, 'b-o', color='red')
    image_name = 'predict\predicted_price.png'
    plt.savefig(image_name)
    image = Image.open(image_name)
    image = ImageTk.PhotoImage(image)
    imgLabel.config(image=image )
    imgLabel.image = image


def GUI():
    windows = tk.Tk()
    windows.title('比特币价格走势')
    windows.geometry('900x600')

    global ave_price_show, origin_price_data_show, predicted_price_show, imgLabel
    ave_price_show = tk.StringVar()
    origin_price_data_show = tk.StringVar()
    predicted_price_show = tk.StringVar()

    B = tk.Button(windows, text='预测下一次交易的价格', command=price_predict)
    B.pack()
    l_ave_price = tk.Label(windows, textvariable=ave_price_show)
    l_origin_price_data = tk.Label(windows, textvariable=origin_price_data_show)
    l_predicted_price = tk.Label(windows, textvariable=predicted_price_show)
    imgLabel = tk.Label(windows)
    l_ave_price.pack()
    l_origin_price_data.pack()
    l_predicted_price.pack()
    imgLabel.pack()
    windows.mainloop()



