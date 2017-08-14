from django.db import models


# Create your models here.
class gainer(models.Model):
    coin = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.coin + ' ' + self.name


class loser(models.Model):
    coin = models.CharField(max_length=20)
    name = models.CharField(max_length=50)


class chartTest(models.Model):
    period = models.CharField(max_length=20)
    close = models.FloatField(max_length=None)


class coinsMain(models.Model):
    coinId = models.CharField(max_length=50, null=True, unique=True)
    coin = models.CharField(max_length=10, null=True, unique=False)
    coinName = models.CharField(max_length=30, null=True, unique=False)
    circSupply = models.FloatField(max_length=None, null=True)
    marketCap = models.FloatField(max_length=None, null=True)
    percentChange1h = models.FloatField(max_length=None, null=True)
    percentChange24h = models.FloatField(max_length=None, null=True)
    percentChange7d = models.FloatField(max_length=None, null=True)

    def __str__(self):
        return self.coin


class pairTickerData(models.Model):
    coinFrom = models.CharField(max_length=5, null=True)
    coinTo = models.CharField(max_length=5, null=True)
    low24hr = models.FloatField(max_length=None, null=True)
    idPol = models.IntegerField(max_length=None, null=True)
    percentChange = models.FloatField(max_length=None, null=True)
    isFrozen = models.IntegerField(max_length=None, null=True)
    quoteVolume = models.FloatField(max_length=None, null=True)
    last = models.FloatField(max_length=None, null=True)
    baseVolume = models.FloatField(max_length=None, null=True)
    high24hr = models.FloatField(max_length=None, null=True)
    lowestAsk = models.FloatField(max_length=None, null=True)
    highestBid = models.FloatField(max_length=None, null=True)
    exchange = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.coinFrom + '_' + self.coinTo
   

class top10MarketCap(models.Model):
    coin = models.CharField(max_length=6, null=True)
    marketCap = models.FloatField(max_length=None, null=True)
    percentChange24h = models.FloatField(max_length=None, null=True)
