from django.db import models

from rest_framework import serializers

class BitCoinPrice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    coin = models.CharField(max_length=100, default='btc')

    def __str__(self):
        return f"{self.price}"

    class Meta:
        ordering = ['timestamp']


class BitcoinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitCoinPrice
        fields = ('timestamp', 'price', 'coin')