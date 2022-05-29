import os
import requests

from django.core.mail import send_mail as django_mail
from django.conf import settings

from bitcoin_app.models import BitCoinPrice
from apscheduler.schedulers.background import BackgroundScheduler

COINGECKO_PUBLIC_ENDPOINT = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"


class BTCScheduler:
    def __init__(self):
        self.url = COINGECKO_PUBLIC_ENDPOINT
        self.background_scheduler = BackgroundScheduler()
        self.max_price = int(os.environ.get('max'))
        self.min_price = int(os.environ.get('min'))
        self.mail_counter = 0

    def _get_btc_usd_price(self):
        api_request = requests.get(self.url)
        try:
            api_request.raise_for_status()
            return api_request.json()
        except:
            return None

    def is_price_crossing_limits(self, price):
        print(f"min:{self.min_price}; max:{self.max_price}; new_price: {price}")
        return (price <= self.min_price) or (price >= self.max_price)

    def send_async_email(self, new_price):
        self.mail_counter += 1
        if self.is_price_crossing_limits(new_price):
            print('Price crossing the range, so sending a mail...')
            self.background_scheduler.add_job(django_mail,
                                              args=(
                                                    'BTC Price Crossing Boundaries',
                                                    f'Current Price: {new_price}',
                                                    'from@example.com',
                                                    [settings.EMAIL_RECEIVER],
                                                ),
                                              kwargs={"fail_silently": False},
                                              id=f"btc_mailer_{self.mail_counter}",
                                              replace_existing=True
                                              )
        else:
            print('Price is in range.')

    def fetch_and_save_btc_price(self):
        # sample response: {"bitcoin":{"usd":29359}}
        btc_data = self._get_btc_usd_price()
        print(f"latest btc data: {btc_data}")
        if btc_data is not None:
            try:
                new_price = btc_data['bitcoin']['usd']
                new_btc_price = BitCoinPrice(price=new_price)
                new_btc_price.save()
                self.send_async_email(new_price)
            except:
                pass


def start():
    freq = int(os.environ.get('scheduler_frequency', '30'))
    print(f"Starting a price fetcher job @{freq}sec frequency.")
    btc_scheduler = BTCScheduler()
    btc_scheduler.background_scheduler.add_job(
        btc_scheduler.fetch_and_save_btc_price,
        "interval",
        seconds=freq,
        id="btc_price_fetcher_0001",
        replace_existing=True
    )
    btc_scheduler.background_scheduler.start()
