from django.urls import path

from . import views

urlpatterns = [
    path('prices/btc', views.PricingAPI.as_view(), name='btc-prices'),
]
