import  numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras import layers
from keras import models
import copy
import csv
# from sklearn import preprocessing
class Model(object):

    def __init__(self):
        self.max = []
        self.min = []
        self.data = []
        # self.delete_0_data()
        self.load_data()
        data, self.max, self.min = data_nornalization(self.data)
        self.data = copy.deepcopy(data)
        self.x_train, self.y_train, self.x_test, self.y_test = self.data_set()

    def delete_0_data(self):
        # 删除交易量为0的数据
        with open('predict\\btc_ustd_data.csv', 'r') as fout, open('predict\\n_btc_ustd_data.csv', 'w', newline='') as fin:
            reader = csv.reader(fout, skipinitialspace=True)
            writer = csv.writer(fin, delimiter=',')
            writer.writerow(next(reader))
            for i in reader:
                if float(i[-1]) != 0.0:
                    writer.writerow(i)
                    print('del')

    def load_data(self):
        # 读入数据
        self.data = pd.read_csv('predict\\btc_ustd_data.csv').iloc[:,1:5].values
        # 对数据预处理，即将买入记为1，卖出记为0。
        for btc_data in self.data:
            if btc_data[0] == 'buy':
                btc_data[0] = 1
            else:
                btc_data[0] = 0
    # def data_nornalization(btc_datas):
        # 数据归一化，提高运算效率。
        # scaler = preprocessing.MinMaxScaler()
        # x_train = scaler.fit_transform(np.array(x_train,dtype=np.float64).reshape(-1,4))
        # y_train = scaler.fit_transform(np.array(y_train,dtype=np.float64).reshape(-1,1)).reshape(1,-1)
        # print(y_train)
        # x_test = scaler.fit_transform(np.array(x_test,dtype=np.float64).reshape(-1,4))
        # y_test = scaler.fit_transform(np.array(y_test,dtype=np.float64).reshape(-1,1)).reshape(1,-1)
        # x_train = np.array(x_train).reshape((-1,80,4))
        # x_test = np.array(x_test).reshape((-1,80,4))
        # return x_train, y_train, x_test, y_test
        # '''
        # 2019/5/5
        # 数据归一化存在bug，
        # 数据经归一化后的形状和原形状相同，
        # 但经过数据归一化后无法进行模型训练。
        # 错误提示：
        # expected dense_1 to have shape (1,) but got array with shape (639920,)
        # 目前未解决。
        #
        # 直接使用原始数据进行训练。
        # (2018/5/6已解决)
        # '''

    def data_set(self):
        # 对数据划分训练集和测试集

        # 训练集
        x_train = []
        y_train = []

        #测试集
        x_test = []
        y_test = []

        train_length = int(0.8*len(self.data))
        for i in range(80,train_length):
            x_train.append(self.data[i-80:i])
            y_train.append(self.data[i][1])
        for i in range(train_length,len(self.data)):
            x_test.append(self.data[i-80:i])
            y_test.append(self.data[i][1])
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_test = np.array(x_test)
        y_test = np.array(y_test)
        return x_train, y_train, x_test, y_test

    def train_model(self):
        # 构建LSTM深度神经网络进行模型训练：

        # 构建LSTM深度神经网络
        model = models.Sequential()
        model.add(layers.LSTM(units=50, return_sequences=True, input_shape=(80,4)))
        model.add(layers.Dropout(0.2))
        model.add(layers.LSTM(units=50, return_sequences=True))
        model.add(layers.Dropout(0,2))
        model.add(layers.LSTM(units=50, return_sequences=True))
        model.add(layers.Dropout(0,2))
        model.add(layers.LSTM(units=50, return_sequences=True))
        model.add(layers.Dropout(0,2))
        model.add(layers.LSTM(units=50))
        model.add(layers.Dropout(0,2))
        model.add(layers.Dense(units=1))
        model.compile(optimizer='rmsprop', loss='mse')
        # 进行训练
        history = model.fit(self.x_train,self.y_train,epochs=20,batch_size=32)

        # 保存模型
        model.save('predict\\btc_usdt_1.h5')

        #数据可视化作图
        loss = history.history['loss']
        epochs = range(1,len(loss)+1)
        plt.plot(epochs, loss, 'b-o', label='Training loss')
        plt.title('Training loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    def test_model(self):
        # 对模型进行验证
        model = models.load_model('predict\\btc_usdt_1.h5')
        y_pre = np.array(model.predict(self.x_test,batch_size=32)).reshape(1,-1)

        #将归一化的数据还原
        y_pre = np.array(y_pre[0]*(self.max[1]-self.min[1]) + self.min[1]).reshape(1,-1)
        n_y_test = np.array(self.y_test*(self.max[1]-self.min[1]) + self.min[1]).reshape(1,-1)

        # 数据可视化作图
        l = range(1, len(n_y_test[0])+1)
        plt.plot(l,n_y_test[0], 'b', color='red', label='True Data')
        plt.plot(l,y_pre[0], 'b', label='Predict Data')
        plt.title('Data')
        plt.xlabel('length')
        plt.ylabel('Data')
        plt.legend()
        plt.show()
    def continue_train(self):
        model = models.load_model('btc_usdt_1.h5')
        model.fit(self.x_train, self.y_train, epochs=20, batch_size=32)
        model.save('btc_usdt_1.h5')


def predict(data):
    model = models.load_model('model\\btc_usdt_1.h5')
    result = np.array(model.predict(data)).reshape(1,-1)
    return result

def data_nornalization(data):
    # 数据归一化
    n_data = np.array(data)
    max = n_data.max(axis=0)
    min = n_data.min(axis=0)
    new_btc_datas = []
    i = 0
    for d in n_data.T:
        da= np.array(d)
        n_d = (da-min[i])/(max[i]-min[i])
        new_btc_datas.append(n_d)
        i += 1
    new_btc_datas = np.array(new_btc_datas).T
    return new_btc_datas, max, min
