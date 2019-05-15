import scipy.io.wavfile as wav
from python_speech_features import mfcc
import numpy as np
import pyaudio
import wave

def Model():
    model = []
    for i in range(1, 5):
        fs, audio = wav.read(str(i)+".wav")
        feature_mfcc = mfcc(audio, samplerate=fs)
        model.append(feature_mfcc)
    return model

def My_Mfcc():
    fs, audio = wav.read("myvoice.wav")
    feature_mfcc = mfcc(audio, samplerate=fs)
    return feature_mfcc

def DTW(mfcc_1,mfcc_2):
    l1 = len(mfcc_1)
    l2 = len(mfcc_2)

    #计算mfcc向量每个维度之间的距离
    dis = []
    for i in range(l1):
        d = []
        for j in range(l2):
            d.append(Distance(mfcc_1[i], mfcc_2[j]))
        dis.append(d)

    #初始化
    cost = np.zeros((l1,l2))
    cost[0][0] = dis[0][0]
    for i in range(1, l1):
        cost[i][0] = cost[i-1][0] + dis[i][0]
    for i in range(1, l2):
        cost[0][i] = cost[0][i-1] + dis[0][i]

    #动态规划求解最短距离
    for i in range(1, l1):
        for j in range(1, l2):
            cost[i][j] = min(cost[i][j-1] + dis[i][j],
                             cost[i-1][j-1]+ dis[i][j]*2,
                             cost[i-1][j] + dis[i][j])
    return cost[l1-1][l2-1]

#求两个向量之间的距离
def Distance(x, y):
    dis = 0
    for i in range(len(x)):
        dis += (x[i]-y[i])**2
    dis = np.sqrt(dis)
    return dis

def record():
    framerate = 16000  # 采样频率 8000 or 16000
    channels = 1  # 声道数
    sampwidth = 2  # 采样字节 1 or 2

    # 实时录音的参数
    CHUNK = 1024  # 录音的块大小
    RATE = 16000  # 采样频率 8000 or 16000
    RECORD_SECONDS = 3  # 录音时长 单位 秒(s)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=channels, rate=framerate, input=True, frames_per_buffer=CHUNK)
    print('开始录音，请说话：')
    frames = []
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('录音结束！')
    wf = wave.open('myvoice.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(frames))
    wf.close()

def Match():
    record()
    model = Model()
    my_mfcc = My_Mfcc()

    flag = 0
    min_dis = DTW(my_mfcc, model[0])
    for i in range(1, len(model)):
        dis = DTW(my_mfcc, model[i])
        if min_dis > dis:
            min_dis = dis
            flag = i

    if flag == 0:
        print('杭州电子科技大学')
    if flag == 1:
        print('浙江理工大学')
    if flag == 2:
        print('浙江音乐学院')
    if flag == 3:
        print('西安电子科技大学')


Match()