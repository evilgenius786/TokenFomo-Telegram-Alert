import datetime
import json
import os
import threading
import time
import traceback

import requests
from telegram.ext import Updater

t = 30
tokenfomo = 'https://tokenfomo.io/api/tokens/'

timeout = 10
api = "your tokenfomo api"
headers = {"Authorization": f"Bearer {api}"}


def get(network):
    r = requests.get(f'{tokenfomo}{network}', headers=headers)
    try:
        js = json.loads(r.text)
    except:
        print("Error", network, r.text)
        js = []
    # print(json.dumps(js[1:10], indent=4))
    return js


def monitor_eth():
    tkn = "your telegram eth channel token"
    chat_id = -1001571309828
    updater = Updater(tkn, use_context=True)
    updater.bot.sendMessage(chat_id=1861985319, text=f"Test")
    chart = 'https://www.dextools.io/app/uniswap/pair-explorer/'
    etherscan = "https://etherscan.io/token/"
    uniswap = "https://app.uniswap.org/#/swap?outputCurrency="
    old = get('eth')
    print("eth Old coins", old)
    while True:
        try:
            print(datetime.datetime.now(), "eth", 'Checking...')
            for coin in get('eth'):
                if coin not in old:
                    data = {
                        "name": coin['name'],
                        "chart": chart + coin['addr'],
                        "etherscan": etherscan + coin['addr'],
                        "uniswap": uniswap + coin['addr']
                    }
                    print(datetime.datetime.now(), "eth", json.dumps(data, indent=4))
                    old.append(coin)
                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['etherscan']}">Etherscan</a>
<a href="{data['uniswap']}">Uniswap</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
        except:
            traceback.print_exc()
        time.sleep(t)


def monitor_bsc():
    tkn = "your telegram bsc channel token"
    chat_id = -1001589924110
    updater = Updater(tkn, use_context=True)
    chart = 'https://poocoin.app/tokens/'
    bscscan = "https://bscscan.com/token/"
    pancakeswap = "https://pancakeswap.finance/swap#/swap?outputCurrency="
    old = get('bsc')
    print("bsc Old coins", old)
    while True:
        try:
            print(datetime.datetime.now(), "bsc", 'Checking...')
            for coin in get('bsc'):
                if coin not in old:
                    data = {
                        "name": coin['name'],
                        "chart": chart + coin['addr'],
                        "BscScan": bscscan + coin['addr'],
                        "PancakeSwap": pancakeswap + coin['addr']
                    }
                    print(datetime.datetime.now(), "bsc", json.dumps(data, indent=4))
                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['BscScan']}">BscScan</a>
<a href="{data['PancakeSwap']}">PancakeSwap</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
                    old.append(coin)
        except:
            traceback.print_exc()
        time.sleep(t)


def monitor_avl():
    tkn = "your telegram avl channel token"
    chat_id = -1001637775983
    updater = Updater(tkn, use_context=True)
    chart = 'https://dexscreener.com/avalanche/'
    explorer = "https://snowtrace.io/token/"
    trade = "https://traderjoexyz.com/#/trade"
    old = get('avax')
    old.pop()
    print("avalanche Old coins", old)
    while True:
        try:
            print(datetime.datetime.now(), "avalanche", 'Checking...')
            for coin in get('avax'):
                if coin not in old:
                    data = {
                        "name": coin['name'],
                        "chart": chart + coin['addr'],
                        "Explorer": explorer + coin['addr'],
                        "Trade": trade + coin['addr']
                    }
                    print(datetime.datetime.now(), "bsc", json.dumps(data, indent=4))
                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['Explorer']}">Explorer</a>
<a href="{data['Trade']}">Trade</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
                    old.append(coin)
        except:
            traceback.print_exc()
        time.sleep(t)


def main():
    os.system('color 0a')
    logo()
    t1 = threading.Thread(target=monitor_eth)
    t1.start()
    time.sleep(t / 2)
    t2 = threading.Thread(target=monitor_bsc())
    t2.start()
    time.sleep(t / 2)
    t3 = threading.Thread(target=monitor_avl())
    t3.start()
    t1.join()
    t2.join()
    t3.join()


def logo():
    print(r"""
    ___________     __                 ___________                    
    \__    ___/___ |  | __ ____   ____ \_   _____/___   _____   ____  
      |    | /  _ \|  |/ // __ \ /    \ |    __)/  _ \ /     \ /  _ \r
      |    |(  <_> )    <\  ___/|   |  \|     \(  <_> )  Y Y  (  <_> )
      |____| \____/|__|_ \\\\___  >___|  /\___  / \____/|__|_|  /\____/ 
                        \/    \/     \/     \/              \/        
=============================================================================
                        TokenFomo monitor tool.
                Developed by: github.com/evilgenius786
=============================================================================
""")


if __name__ == '__main__':
    main()
