from decimal import Decimal

from celery import shared_task

from currency import model_choices as mch

from django.conf import settings
from django.core.mail import send_mail

import requests


def round_decimal(value: str) -> Decimal:
    places = Decimal(10) ** -2
    return Decimal(value).quantize(places)


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source

    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'UAH': mch.RateType.UAH,
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
        'BTC': mch.RateType.BTC,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK)[0]

    for rate in rates:
        # if rate['ccy'] not in available_currencies:
        #     continue
        # currency_type = rate['ccy']
        currency_type = available_currencies.get(rate['ccy'])  # the same as above
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['base_ccy'])

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_monobank():
    from currency.models import Rate, Source

    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        980: mch.RateType.UAH,
        840: mch.RateType.USD,
        978: mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.MONOBANK)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['currencyCodeA'])
        base_currency_type = available_currencies.get(rate['currencyCodeB'])
        if rate['currencyCodeB'] != 980:
            continue
        sale = rate.get('rateSell')
        if not sale:
            continue
        else:
            sale = round_decimal(sale)
        buy = rate.get('rateBuy')
        if not buy:
            continue
        else:
            buy = round_decimal(buy)

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_vkurse():
    from currency.models import Rate, Source

    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'Dollar': mch.RateType.USD,
        'Euro': mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.VKURSE)[0]

    for key, value in rates.items():
        currency_type = available_currencies.get(key)
        if not currency_type:
            continue
        base_currency_type = 'UAH'

        sale = round_decimal(value['sale'])
        buy = round_decimal(value['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_getgeoapi():
    from currency.models import Rate, Source

    url = 'https://api.getgeoapi.com/v2/currency/convert'
    api_key = settings.GETGEOAPI_KEY
    available_currencies = {
        'UAH': mch.RateType.UAH,
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    result = []
    for currency1 in available_currencies.keys():
        for currency2 in available_currencies.keys():
            if currency1 == currency2:
                continue
            params = {
                'api_key': api_key,
                'from': currency1,
                'to': currency2,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            rates = response.json()
            result.append(rates)

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.GETGEOAPI)[0]

    result_rates = []
    for rate in result:
        d = {}
        d['base_currency_type'] = rate['base_currency_code']
        for k, v in rate['rates'].items():
            d['currency_type'] = k
            d['rate'] = v.get('rate')
            result_rates.append(d.copy())

    rate_list = []
    d2 = {}
    for i in result_rates:
        for j in result_rates:
            if i['base_currency_type'] == j['currency_type'] and j['base_currency_type'] == i['currency_type']\
                    and i['base_currency_type'] == 'UAH':
                d2['base_currency_type'] = i['base_currency_type']
                d2['currency_type'] = i['currency_type']
                d2['sale'] = float(i['rate']) * 1000
                d2['buy'] = j['rate']
            else:
                continue
        rate_list.append(d2.copy())
    rates = [i for n, i in enumerate(rate_list) if i not in rate_list[n + 1:]]

    for i in rates:
        currency_type = i['currency_type']
        base_currency_type = i['base_currency_type']
        sale = round_decimal(i['sale'])
        buy = round_decimal(i['buy'])

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_fixer():
    from currency.models import Rate, Source

    url = 'https://api.apilayer.com/fixer/convert'
    headers = {
        'apikey': settings.FIXER_API_KEY,
    }

    available_currencies = {
        'UAH': 'UAH',
        'USD': 'USD',
        'EUR': 'EUR',
        'BTC': 'BTC',
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.FIXER)[0]

    rates_list = []
    for currency1 in available_currencies.keys():
        for currency2 in available_currencies.keys():
            if currency1 == currency2:
                continue
            params = {
                'from': currency1,
                'to': currency2,
                'amount': 1,
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            rates = response.json()
            rates_list.append(rates)

    rates = []
    d = {}
    for i in rates_list:
        for j in rates_list:
            if i['query']['from'] == j['query']['to'] and j['query']['from'] == i['query']['to']\
                    and i['query']['from'] == 'UAH':
                d['base_currency_type'] = i['query']['from']
                d['currency_type'] = i['query']['to']
                d['sale'] = float(i['info']['rate']) * 1000
                d['buy'] = j['info']['rate']
            else:
                continue
        rates.append(d.copy())

    for i in rates:
        currency_type = i['currency_type']
        base_currency_type = i['base_currency_type']
        sale = round_decimal(i['sale'])
        buy = round_decimal(i['buy'])

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_freecurrconv():
    from currency.models import Rate, Source

    url = 'https://free.currconv.com/api/v7/convert'
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
        'BTC': mch.RateType.BTC,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.FREECURRCONV)[0]

    result = []
    for currency in available_currencies.keys():
        params = {
            'q': f'{currency}_UAH,UAH_{currency}',
            'apiKey': settings.CUR_CONV_API_KEY,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        rates = response.json()
        result.append(rates)

    rate_list = []
    for rate in result:
        d = {}
        for v in rate['results'].values():
            if v['fr'] == 'UAH':
                d['base_currency_type'] = v['fr']
                d['currency_type'] = v['to']
                d['sale'] = float(v['val']) * 1000
            if v['to'] == 'UAH':
                d['base_currency_type'] = v['to']
                d['currency_type'] = v['fr']
                d['buy'] = v['val']
        rate_list.append(d)

    for i in rate_list:
        currency_type = i['currency_type']
        base_currency_type = i['base_currency_type']
        sale = round_decimal(i['sale'])
        buy = round_decimal(i['buy'])

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def contact_us_async(subject, email_from, message):
    subject = f"Contact us: {subject}"
    message = f'''
        Support Email
        From: {email_from}
        Message: {message}
        '''
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject,
        message,
        email_from,
        [email_from],
        fail_silently=False,
    )
