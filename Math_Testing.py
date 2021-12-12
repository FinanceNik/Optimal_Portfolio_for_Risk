import pandas as pd
import json
import os
from datetime import datetime


def historic():
    f1 = open('historic token price osmo.json')
    data = json.load(f1)
    os.system('touch historic_token_price.txt')
    os.system(f'echo "time, close, high, low, open" >> historic_token_price.txt')
    for i in range(200):
        try:
            time = data[i]['time']
            time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
            close = data[i]['close']
            high = data[i]['high']
            low = data[i]['low']
            open = data[i]['open']
            text = f"{time}, {close}, {high}, {low}, {open}"
            os.system(f'echo {text} >> historic_token_price.txt')
        except:
            pass

    os.system('mv historic_token_price.txt historic_token_price.csv')


def liquidity():
    f1 = open('Liquidty historical.json')
    data = json.load(f1)
    os.system('touch liquidity_historical.txt')
    os.system(f'echo "time, value" >> liquidity_historical.txt')
    for i in range(1000):
        try:
            time = data[i]['time']
            value = data[i]['value']
            text = f"{time}, {value}"
            os.system(f'echo {text} >> liquidity_historical.txt')
        except:
            pass

    os.system('mv liquidity_historical.txt liquidity_historical.csv')


def volume():
    f1 = open('volume histroical .json')
    data = json.load(f1)
    os.system('touch volume_historical.txt')
    os.system(f'echo "time, value" >> volume_historical.txt')
    for i in range(1000):
        try:
            time = data[i]['time']
            value = data[i]['value']
            text = f"{time}, {value}"
            os.system(f'echo {text} >> volume_historical.txt')
        except:
            pass

    os.system('mv volume_historical.txt volume_historical.csv')


def pools():
    f1 = open('response_1639217583822.json')
    data = json.load(f1)['data']
    os.system('touch pools.txt')
    os.system(f'echo "time, close, high, low, open" >> pools.txt')
    for i in range(1000):
        try:
            a = data[i]['pool_address']
            b = data[i]['pool_id']
            c = data[i]['base_name']
            d = data[i]['base_symbol']
            e = data[i]['base_address']
            f = data[i]['quote_name']
            g = data[i]['quote_symbol']
            h = data[i]['quote_address']
            z = data[i]['price']
            j = data[i]['base_volume_24h']
            k = data[i]['quote_volume_24h']
            l = data[i]['volume_24h']
            m = data[i]['volume_7d']
            n = data[i]['liquidity']
            o = data[i]['liquidity_atom']
            text = f"{a}, {b}, {c}, {d}, {e}, {f}, {g}, {h}, {z}, {j}, {k}, {l}, {m}, {n}, {o}"
            os.system(f'echo {text} >> pools.txt')
        except:
            pass

    os.system('mv pools.txt pools.csv')


pools()




