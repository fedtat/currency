from datetime import datetime, timedelta

from currency import model_choices as mch
from currency.models import Rate, Source

from django.core.management.base import BaseCommand
from django.utils import timezone

import requests


class Command(BaseCommand):
    help = 'Parse Privatbank archive rates'  # noqa: A003

    def handle(self, *args, **options):
        available_currencies = {
            'UAH': mch.RateType.UAH,
            'USD': mch.RateType.USD,
            'EUR': mch.RateType.EUR,
            'BTC': mch.RateType.BTC,
        }
        source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK)[0]

        base_date = datetime.today() - timedelta(days=1)
        days_num = 4 * 365
        dates_list = [base_date - timedelta(days=x) for x in range(days_num)]
        for date in dates_list:
            params = {
                'date': date.strftime("%d.%m.%Y")
            }
            url = 'https://api.privatbank.ua/p24api/exchange_rates?json'
            response = requests.get(url, params=params)
            result = response.json()

            for rate in response.json():
                c_date = result['date']
                created = datetime.strptime(c_date, '%d.%m.%Y').strftime('%Y-%m-%d %H:%M:%S')
                created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
                tz = timezone.get_current_timezone()
                timezone_dt = timezone.make_aware(created, tz, True)
                for i in result['exchangeRate']:
                    if available_currencies.get(i['baseCurrency']) == available_currencies.get(i.get('currency')):
                        continue
                    else:
                        base_currency_type = available_currencies.get(i['baseCurrency'])
                        currency_type = available_currencies.get(i.get('currency'))
                        if not available_currencies.get(i.get('currency')):
                            continue
                        sale = i.get('saleRate')
                        buy = i.get('purchaseRate')

                        last_rate = Rate.objects \
                            .filter(source=source, type=currency_type, created=timezone_dt) \
                            .order_by('-created').first()

                        if (last_rate is None or
                                last_rate.sale != sale and
                                last_rate.buy != buy and
                                last_rate.created != timezone_dt):
                            record = Rate.objects.create(
                                type=currency_type,
                                base_type=base_currency_type,
                                sale=sale,
                                buy=buy,
                                source=source,

                            )
                            rate_id = record.id
                            Rate.objects.filter(pk=rate_id).update(created=timezone_dt)
