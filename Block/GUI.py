import tkinter
from tkinter import messagebox, Toplevel, ttk, Text
from price_predict import *

class GUI(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("区块链价格预测系统")
        self.root.geometry('370x370')
        self.dataGet_button = tkinter.Button(self.root, command=self.dataGet, text='最新数据', width=25, height=3)
        self.dataAnalysis_button = tkinter.Button(self.root, command=self.dataAnalysis, text='分析数据', width=25, height=3)
        self.PricePredict_button = tkinter.Button(self.root, command=self.Predict, text='价格预测', width=25, height=3)
    def GuiArrang(self):
        self.dataGet_button.place(x=100,y=50)
        self.dataAnalysis_button.place(x=100,y=120)
        self.PricePredict_button.place(x=100, y=190)
    def dataGet(self):
        self.top = Toplevel()
        self.top.title = ('数据获取')
        self.top.geometry('600x700')
        tmp = None
        def arrang():
            currency1Chosen.place(x=60, y=20)
            currency1Chosen.current(0)
            currency2Chosen.place(x=280, y=20)
            currency2Chosen.current(0)
            label_to.place(x=220, y=20)
            Submit_button.place(x=400, y=20)
            Drawing_button.place(x=500, y=20)
            self.tree.column("a", width=125, anchor="center")
            self.tree.column("b", width=100, anchor="center")
            self.tree.column("c", width=100, anchor="center")
            self.tree.column("d", width=100, anchor="center")
            self.tree.column("e", width=100, anchor="center")
            self.tree.heading("a", text="订单时间")
            self.tree.heading("b", text="买卖类型")
            self.tree.heading("c", text="币种单价")
            self.tree.heading("d", text="成交币种数量")
            self.tree.heading("e", text="订单总额")
            self.tree.place(x=38, y=80)
            vbar.place(x=695, y=30, height=550)

        def dataCrawl():
            rootUrl = 'https://data.gateio.co/api2/1/tradeHistory/'
            currency1.get()
            url = rootUrl + currency1.get() + '_' +currency2.get()
            browsers = requests.get(url).json()
            items = None
            if (browsers["result"] == "true"):
                items = browsers["data"]
            else:
                messagebox.showinfo(title='error', message='Please Retry')
            for _ in map(self.tree.delete, self.tree.get_children("")):
                pass
            for item in items:
                self.tree.insert("", "end", values=(item["date"], item["type"], item["rate"], item["amount"], item["total"]))
            Drawing_button['state'] = 'active'

        def dataDrawing():
            messagebox.showinfo(title='Waiting~', message='I am drawing!')
        currency1 = tkinter.StringVar()
        currency2 = tkinter.StringVar()
        currency1Chosen = ttk.Combobox(self.top, width=12, textvariable=currency1)
        currency1Chosen['values'] = ('eth', 'btc')
        label_to = tkinter.Label(self.top, text='to')
        currency2Chosen = ttk.Combobox(self.top, width=12, textvariable=currency2)
        currency2Chosen['values'] = ('usdt', 'cnyx')
        Submit_button = tkinter.Button(self.top, command=dataCrawl, text='开始抓取')
        Drawing_button = tkinter.Button(self.top, command=dataDrawing, text='绘制图表', state='disabled')
        self.tree = ttk.Treeview(self.top, show="headings", height=28, columns=("a", "b", "c", "d", "e"))
        vbar = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        arrang()

    def Predict(self):
        self.top = Toplevel()
        self.top.title = ('数据获取')
        self.top.geometry('600x400')
        ave_price_show = tkinter.StringVar()
        origin_price_data_show = tkinter.StringVar()
        predicted_price_show = tkinter.StringVar()
        self.i = 0
        def price_predict():
            url = 'https://data.gateio.co/api2/1/tradeHistory/btc_usdt'
            data = []
            load_btc_data(url, data)
            data_process(data)
            origin_price_data = copy.deepcopy(np.array(data).T[1])
            # 对数据归一化
            new_btc_data, max, min = data_nornalization(data)
            new_btc_data = np.array(new_btc_data).reshape((1, 80, 4))
            ave_price = origin_price_data.mean()
            # 预测价格
            result = predict(new_btc_data)
            predicted_price = result[0][0] * (max[1] - min[1]) + min[1]
            ave_price_show.set('最新80笔交易的平均价格:' + str(ave_price))
            origin_price_data_show.set('当前最新价格:' + str(origin_price_data[-1]))
            predicted_price_show.set('预测的下一次交易的价格:' + str(predicted_price))
            print('最新80笔交易的平均价格:{}'.format(ave_price))
            print('当前最新价格：{}'.format(origin_price_data[-1]))
            print('预测的下一次交易的价格:{}'.format(predicted_price))
            # 可视化
            l1 = range(1, len(origin_price_data) + 1)
            plt.figure()
            plt.plot(l1, origin_price_data, 'b-', color='blue')
            l2 = [80, 81]
            predict_data = [origin_price_data[-1], predicted_price]
            plt.plot(l2, predict_data, 'b-o', color='red')
            image_name = 'predict\predicted_price' + str(self.i) + '.png'
            self.i += 1
            plt.savefig(image_name)
            image = self.Png_To_Gif(image_name)
            self.imgLabel.config(image=image)
            self.imgLabel.image = image
            self.top.update_idletasks()
            self.top.after(100)

        B = tkinter.Button(self.top, text='预测下一次交易的价格', command=price_predict)
        B.pack()
        l_ave_price = tkinter.Label(self.top, textvariable=ave_price_show)
        l_origin_price_data = tkinter.Label(self.top, textvariable=origin_price_data_show)
        l_predicted_price = tkinter.Label(self.top, textvariable=predicted_price_show)
        self.imgLabel = tkinter.Label(self.top)
        l_ave_price.pack()
        l_origin_price_data.pack()
        l_predicted_price.pack()
        self.imgLabel.pack()

    def Png_To_Gif(self,image_name):
        image = Image.open(image_name)
        (x,y) = image.size
        x_s = int(x / 2)
        y_s = int(y / 2)
        image = image.resize((x_s, y_s), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image

    def dataAnalysis(self):
        self.top = Toplevel()
        self.top.title = ('数据分析')
        self.top.geometry('700x700')
        canvas = tkinter.Canvas(self.top, width=800, height=800, scrollregion=(0, 0, 1400, 1400))  # 创建canvas
        canvas.place(x=0, y=0)  # 放置canvas的位置
        frame = tkinter.Frame(canvas, width=1400, height=1400)  # 把frame放在canvas里
        frame.place(x=0, y=0)  # frame的长宽，和canvas差不多的
        vbar = tkinter.Scrollbar(canvas, orient='vertical')  # 竖直滚动条
        vbar.place(x=680, width=20, height=700)
        vbar.configure(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)  # 设置
        image1 = self.Png_To_Gif('data_analyse\\all_trade_all.png')
        image2 = self.Png_To_Gif('data_analyse\\all_trade_big_volume.png')
        image3 = self.Png_To_Gif('data_analyse\\buy_all.png')
        image4 = self.Png_To_Gif('data_analyse\\buy_big_colume.png')
        image5 = self.Png_To_Gif('data_analyse\\sell_all.png')
        image6 = self.Png_To_Gif('data_analyse\\sell_big_volume.png')
        image7 = self.Png_To_Gif('data_analyse\\list1.png')
        image8 = self.Png_To_Gif('data_analyse\\list2.png')
        self.img_label1 = tkinter.Label(frame, image=image1)
        self.img_label2 = tkinter.Label(frame, image=image2)
        self.img_label3 = tkinter.Label(frame, image=image3)
        self.img_label4 = tkinter.Label(frame, image=image4)
        self.img_label5 = tkinter.Label(frame, image=image5)
        self.img_label6 = tkinter.Label(frame, image=image6)
        self.img_label7 = tkinter.Label(frame, image=image7)
        self.img_label8 = tkinter.Label(frame, image=image8)
        self.img_label1.image = image1
        self.img_label2.image = image2
        self.img_label3.image = image3
        self.img_label4.image = image4
        self.img_label5.image = image5
        self.img_label6.image = image6
        self.img_label7.image = image7
        self.img_label8.image = image8
        self.img_label1.place(x=0, y=0)
        self.img_label2.place(x=350, y=0)
        self.img_label3.place(x=0, y=250)
        self.img_label4.place(x=350, y=250)
        self.img_label5.place(x=0, y=500)
        self.img_label6.place(x=350, y=500)
        self.img_label7.place(x=0, y=750)
        self.img_label8.place(x=0, y=860)
        text = '从上面的六个图和两个价格差的对比表格可以明显看出：\n' \
               '在所有交易中，所有交易平均的价格差方差为75.5788，而大额交易的价格差方差为78.9996，由此可以看出大额交易使得价格的变化波动加剧，但总体来说对价格的变化并不是很明显,交易后比交易前价格平均上升0.20左右。但对买入和卖出的交易分别分析。可以发现，大额交易对价格有非常明显的影响。\n' \
               '在买入交易中，平均的价格差方差为151.0677而大额交易前后的价格差方差达到了163.9778。可见在买入交易中，大额交易前后价格的波动加剧。而在价格差平均值方面，所有买入的交易前后价格差基本没变化，而在大额交易后，价格上升了0.31。由此可以发现：\n' \
               '大额买入显著提升了比特币的价格。\n' \
               '在卖出交易中，平均的价格差方差为155.8411而大额交易前后的价格差方差达到了166.9491。可见在卖出交易中，大额交易前后价格的波动加剧。而在价格差平均值方面，两者的价格差也基本持平。\n' \
               '最终我们得出结论： 大额交易使得交易价格的波动加剧，而大额交易对价格的影响主要体现在买入交易中，大额买入显著提升了比特币的价格。\n'
        label1 = tkinter.Label(frame, text=text, width=800, height=30, wraplength=600, justify='left', anchor='nw')
        label1.place(x=0, y=980)
        canvas.create_window((700,700),window=frame)





def main():
    g = GUI()
    g.GuiArrang()
    tkinter.mainloop()

if __name__ == '__main__':
    main()