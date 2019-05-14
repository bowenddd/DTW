import requests
import csv
def load_btc_data(furl, data):
    tradeID = 145979000
    for i in range(1000):
        url = furl + '/' + str(tradeID)
        r = requests.get(url)
        content = r.json()
        datas = content['data']
        if datas:
            for d in datas:
                data['date'].append(d['date'])
                data['type'].append(d['type'])
                data['rate'].append(d['rate'])
                data['amount'].append(d['amount'])
                data['total'].append(d['total'])
            tradeID = content['data'][-1]['tradeID']
            print('\r当前爬取数据进度:{:.2f}%'.format((i + 1)* 100 / 800), end='')
        else:
            print("\n爬取结束")
            break
    print('\n')

def save_to_csv(data):
    fin = open('data_analyse\\btc_ustd_data.csv', 'w', newline='')
    try:
        writer = csv.writer(fin, dialect='excel')
        head = ['data', 'type', 'rate', 'amount', 'total']
        writer.writerow(head)
        for i in range(len(data['date'])):
            content = [data['date'][i], data['type'][i], data['rate'][i], data['amount'][i], data['total'][i]]
            print(content)
            writer.writerow(content)
            print('\r当前写入csv进度:{:.2f}%'.format(i * 100 / len(data['date'])), end='')
        print('\n')
        fin.close()
        print('写入csv成功')
        print('共写入{}个数据'.format(len(data['date'])))
    except Exception:
        print('写入csv失败')
        fin.close()
def download_data():
    url = 'https://data.gateio.co/api2/1/tradeHistory/btc_usdt'
    data = {'date': [], 'type': [], 'rate': [], 'amount': [], 'total': []}
    load_btc_data(url, data)
    save_to_csv(data)

download_data()