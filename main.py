import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coinvizio.settings")
django.setup()

from dashboard import models
from django.db import transaction, models
from dashboard.models import pairTickerData, coinsMain, top10MarketCap

import urllib.request
import json


def checkTableEmpty(tbl):
    if tbl.objects.exists():
        return 0
    else:
        return 1


def popOrUpdateTop10MarketCapData():
    allObjects = coinsMain.objects.order_by(
        '-marketCap').values('coin', 'marketCap', 'percentChange24h')
    i = 0
    top10Other = {}
    sumOthers = 0
    for obj in allObjects:
        if i <= 9 and obj['marketCap'] is not None:
            # print(allObjects[i]['coin'])
            top10Other.update(
                {obj['coin']: [obj['marketCap'], obj['percentChange24h']]})
            i += 1
        else:
            if i >= 10 and obj['marketCap'] is not None:
                sumOthers += obj['marketCap']
                i += 1

    top10Other.update({'Others': [sumOthers, 0]})

    objs = []
    for k, v in top10Other.items():
        # print(k)
        obj = top10MarketCap(
            coin=k,
            marketCap=v[0],
            percentChange24h=v[1]
        )
        objs.append(obj)

    if checkTableEmpty(top10MarketCap) == 1:
        top10MarketCap.objects.bulk_create(objs)
        print('Top10MarketCapData populated succesfully')
    else:
        for obj in objs:
            top10MarketCap.objects.filter(coin=obj.coin).update(marketCap=obj.marketCap, percentChange24h=obj.percentChange24h)
        print('Top10MarketCapData updated succesfully')


def popOrUpdateCoinsMain():
    objs = []
    req = urllib.request.Request(
            'https://api.coinmarketcap.com/v1/ticker/', headers={'User-Agent': 'Mozilla/5.0'}
            )
    apiResponseData = json.loads(urllib.request.urlopen(req).read().decode('windows-1252'))
    # print(apiResponseData)
    isCoinsMainEmpty = checkTableEmpty(coinsMain)
    for coin in apiResponseData:
        if int(coin['rank']) <= 1000:
            obj = coinsMain(
                coinId=coin['id'],
                coin=coin['symbol'],
                coinName=coin['name'],
                circSupply=coin['available_supply'],
                marketCap=coin['market_cap_usd'],
                percentChange1h=coin['percent_change_1h'],
                percentChange24h=coin['percent_change_24h'],
                percentChange7d=coin['percent_change_7d']
                )
            objs.append(obj)
    if isCoinsMainEmpty == 1:
        coinsMain.objects.bulk_create(objs)
        print('coinsMain populated succesfully')
    else:
        for obj in objs:
            coinsMain.objects.filter(coinId=obj.coinId).update(coin=obj.coin, coinName=obj.coinName, circSupply=obj.circSupply, marketCap=obj.marketCap, percentChange1h=obj.percentChange1h, percentChange24h=obj.percentChange24h, percentChange7d=obj.percentChange7d)
        print('coinsMain updated succesfully')

while True:
    popOrUpdateCoinsMain()
    popOrUpdateTop10MarketCapData()
    time.sleep(20)
  