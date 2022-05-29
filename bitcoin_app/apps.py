from django.apps import AppConfig


class BitcoinAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bitcoin_app'

    def ready(self):
        print('Bitcoin App is getting ready with a scheduler job...')
        from bitcoin_app.btc_scheduler import price_fetcher
        price_fetcher.start()
