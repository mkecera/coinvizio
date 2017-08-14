# market data updates
from poloniex import Poloniex
import psycopg2

# update poloniex data
polo = Poloniex()
poloMarkets = ['BTC_ETH', 'BTC_GNT']
poloPeriods = [300]
marketData = {}
candleData = {}

for period in poloPeriods:
    for market in poloMarkets:
        marketData[market] = polo.returnChartData(market, period=period)
    candleData[period] = marketData

print(candleData)