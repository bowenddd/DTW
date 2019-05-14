import csv
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='C:\Windows\Fonts\msyh.ttc',size=12)
def analyse(fname, choice='all_volume'):
    mylist = []
    datas = []
    iteration = None
    with open(fname,'r') as fout:
        reader = csv.reader(fout,skipinitialspace=True)
        for i,content in enumerate(reader):
            if i == 0:
                continue
            datas.append(content)
            if float(content[-1]) >= 1000.0:
                mylist.append(i-1)
    if choice == 'big_volume':
        n_list = []
        t = 0
        for i in range(len(mylist)):
            if mylist[i] < 100 or mylist[i] > len(datas) - 100:
                continue
            if mylist[i] - t < 100:
                continue
            t = mylist[i]
            n_list.append(mylist[i])
        iteration = n_list
    if choice =='all_volume':
        r_list = list(range(101,len(datas)-103))
        random.shuffle(r_list)
        # iteration = range(101, len(datas)-3, 100)
        iteration = r_list[:8000]
    ave_front = []
    ave_back = []
    for i in list(iteration):
        data = []
        s_datas_f = datas[i-101:i]
        s_datas_b = datas[i+1:i+102]
        for s_data in s_datas_f:
            data.append(float(s_data[-3]))
        data = np.array(data)
        ave_front.append(data.mean())
        data = []
        for s_data in s_datas_b:
            data.append(float(s_data[-3]))
        data = np.array(data)
        ave_back.append(data.mean())
    ave_front = np.array(ave_front)
    ave_back = np.array(ave_back)
    c = ave_back - ave_front
    print('平均值{}'.format(c.mean()))
    print('方差{}'.format(c.var()))
    print('标准差{}'.format(c.std()))
    c.reshape((1,-1))
    print(c.shape)
    x = np.array(range(1,len(c)+1))

    print(x.shape)
    plt.plot(x,c)
    plt.title('所有交易中任取一次交易，该交易后100次交易平均值与前100次交易的平均值的差', fontproperties=font)
    plt.xlabel('交易数', fontproperties=font)
    plt.ylabel('价格差', fontproperties=font)
    plt.show()

def uncouple(rfname, wfname):
    with open(rfname, 'r') as fout, open(wfname, 'w', newline='') as fin:
        reader = csv.reader(fout, skipinitialspace=True)
        writer = csv.writer(fin, delimiter=',')
        writer.writerow(next(reader))
        for i in reader:
            if i[1] == wfname.split('.')[0]:
                writer.writerow(i)


analyse(fname='BTCM.csv', choice='all_volume')

