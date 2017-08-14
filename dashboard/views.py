from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from dashboard.models import coinsMain, top10MarketCap
from itertools import chain


# Create your views here.
# def index(request):
#     from .models import gainer
#     allGainers = gainer.objects.all()
#     context = {
#         'allGainers': allGainers,
#     }
#     return render(request, 'dashboard/index.html', context)


def index(request):
    topGainers = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('-percentChange24h')
    topGainers = topGainers.exclude(marketCap__isnull=True)[:10]
    topLosers = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('percentChange24h')
    topLosers = topLosers.exclude(marketCap__isnull=True)[:10]
    topGainers7d = coinsMain.objects.exclude(percentChange7d__isnull=True).order_by('-percentChange7d')
    topGainers7d = topGainers7d.exclude(marketCap__isnull=True)[:10]
    topLosers7d = coinsMain.objects.exclude(percentChange7d__isnull=True).order_by('percentChange7d')
    topLosers7d = topLosers7d.exclude(marketCap__isnull=True)[:10]
    
    context = {
        'topGainers': topGainers,
        'topLosers': topLosers,
        'topGainers7d': topGainers7d,
        'topLosers7d': topLosers7d,
    }
    return render(request, 'dashboard/index.html', context)


def detail(request, coinId):
    from .models import gainer
    gainer = get_object_or_404(gainer, id=coinId)
    return render(request, 'dashboard/detail.html', {'gainer': gainer})


class pieChartDataCoinMarketCap(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = top10MarketCap.objects.order_by('-marketCap').values_list('coin', flat=True)
        default = top10MarketCap.objects.order_by('-marketCap').values_list('marketCap', flat=True)
        data = {
            "labels": labels,
            "default": default
        }
        return Response(data)


class barChartData24hChange(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labelsmax = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('-percentChange24h').values_list('coin', flat=True)[:10]
        defaultmax = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('-percentChange24h').values_list('percentChange24h', flat=True)[:10]
        labelsmin = reversed(coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('percentChange24h').values_list('coin', flat=True)[:10])
        defaultmin = reversed(coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('percentChange24h').values_list('percentChange24h', flat=True)[:10])
        labels = list(chain(labelsmax, labelsmin))
        default = list(chain(defaultmax, defaultmin))
        data = {
            "labels": labels,
            "default": default
        }
        return Response(data)
    

class barChartDataTopCapChange(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = top10MarketCap.objects.exclude(coin='Others').order_by('-marketCap').values_list('coin', flat=True)
        default = top10MarketCap.objects.exclude(coin='Others').order_by('-marketCap').values_list('percentChange24h', flat=True)
        data = {
            "labels": labels,
            "default": default
        }
        return Response(data)


class tableDataTopGainers(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('-percentChange24h').values_list('coin', flat=True)[:10]
        default = coinsMain.objects.exclude(percentChange24h__isnull=True).order_by('-percentChange24h').values_list('percentChange24h', flat=True)[:10]
        data = {
            "labels": labels,
            "default": default
        }
        return Response(data)
