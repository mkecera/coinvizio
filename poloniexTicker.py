from multiprocessing import Process, Queue
from multiprocessing.dummy import Process as Thread

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

import poloniex

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coinvizio.settings")
django.setup()
from dashboard import models
from django.db import transaction, models
from dashboard.models import pairTickerData, coinsMain

queue = Queue()


class TickPitcher(ApplicationSession):
    """ WAMP application """
    @inlineCallbacks
    def onJoin(self, details):
        yield self.subscribe(self.onTick, 'ticker')
        print('Subscribed to Ticker')

    def onTick(self, *tick):
        queue.put(tick)

    def onDisconnect(self):
        if reactor.running:
            reactor.stop()


class Ticker(object):

    def __init__(self):
        self.ticker = poloniex.Poloniex().returnTicker()
        self._appRunner = ApplicationRunner(
            u"wss://api.poloniex.com:443", u"realm1"
        )
        self._appProcess, self._tickThread = None, None
        self._running = False

    def __call__(self):
        return self.ticker

    def tickCatcher(self):
        print("Catching...")
        while self._running:
            try:
                tick = queue.get(timeout=1)
            except:
                continue
            else:
                self.ticker[tick[0]] = {
                    'last': tick[1],
                    'lowestAsk': tick[2],
                    'highestBid': tick[3],
                    'percentChange': tick[4],
                    'baseVolume': tick[5],
                    'quoteVolume': tick[6],
                    'isFrozen': tick[7],
                    'high24hr': tick[8],
                    'low24hr': tick[9],
                    'id': self.ticker[tick[0]]['id']
                }
        print("Done catching...")

    def start(self):
        """ Start the ticker """
        print("Starting ticker")
        self._appProcess = Process(
            target=self._appRunner.run,
            args=(TickPitcher,)
        )
        self._appProcess.daemon = True
        self._appProcess.start()
        self._running = True
        print('TICKER: tickPitcher process started')
        self._tickThread = Thread(target=self.tickCatcher)
        self._tickThread.deamon = True
        self._tickThread.start()
        print('TICKER: tickCatcher thread started')

    def stop(self):
        """ Stop the ticker """
        print("Stopping ticker")
        self._appProcess.terminate()
        print("Joining Process")
        self._appProcess.join()
        print("Joining thread")
        self._running = False
        self._tickThread.join()
        print("Ticker stopped.")


def checkTableEmpty(tbl):
    if tbl.objects.exists():
        return 0
    else:
        return 1


def popOrUdatePairTickerData(isEmpty, inputDict):
    if isEmpty == 1:
        objs = []
        for k, v in inputDict.items():
            tempDict = {'coinFrom': k.split(
                "_", 1)[0], 'coinTo': k.split("_", 1)[1]}
            v.update(tempDict)
            # print(tempDict['coinTo'])
            # coin = coinsMain.objects.get(coin=tempDict['coinTo'])
            obj = pairTickerData(
                coinFrom=v['coinFrom'],
                coinTo=v['coinTo'],
                low24hr=v['low24hr'],
                idPol=v['id'],
                percentChange=v['percentChange'],
                isFrozen=v['isFrozen'],
                quoteVolume=v['quoteVolume'],
                last=v['last'],
                baseVolume=v['baseVolume'],
                high24hr=v['high24hr'],
                lowestAsk=v['lowestAsk'],
                highestBid=v['highestBid'],
                exchange="Pol"
            )
            objs.append(obj)
        pairTickerData.objects.bulk_create(objs)


# def bulkInsertCoins(isEmpty, inputDict):
#     if isEmpty == 1:
#         objs = []
#         s = set(k.split("_", 1)[1] for k in inputDict.keys())
#         for x in s:
#             obj = coinsMain(
#                 coin=x,
#                 circSupply=100
#             )
#             objs.append(obj)
#         coinsMain.objects.bulk_create(objs)


if __name__ == '__main__':
    import time
    ticker = Ticker()
    ticker.start()
    for i in range(1):
        # print(ticker())
        # isTableEmpty = misc.checkTableEmpty(coinsMain)
        # bulkInsertCoins(isTableEmpty, ticker())
        isTableEmpty = checkTableEmpty(pairTickerData)
        popOrUdatePairTickerData(isTableEmpty, ticker())
        time.sleep(1)
    ticker.stop()
    print("Done")
