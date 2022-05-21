from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_monobank, parse_privatbank, parse_vkurse


def test_parse_privatbank(mocker):
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "29.25490", "sale": "32.05128"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.76880", "sale": "33.78378"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.32000", "sale": "0.35001"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "27815.6784", "sale": "30743.6446"}
    ]
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 1

    # second exec - no change
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11',)
    assert request_get_mock.call_args[1] == {}

    # third exec - change one rate
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "30.25490", "sale": "32.05128"}
    ]
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock_2.call_count == 0
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 4
    assert request_get_mock_2.call_count == 1


def test_parse_monobank(mocker):
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1653123607, "rateBuy": 29.5, "rateSell": 32},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1653123607, "rateBuy": 31.1,
         "rateSell": 33.7998},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1653081007, "rateBuy": 1.047,
         "rateSell": 1.067},
    ]
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # second exec - no change
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.monobank.ua/bank/currency',)
    assert request_get_mock.call_args[1] == {}

    # third exec - change one rate
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1653123607, "rateBuy": 29.5, "rateSell": 34}
    ]
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock_2.call_count == 0
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1


def test_parse_vkurse(mocker):
    response_json = {
        "Dollar": {
            "buy": "35.00",
            "sale": "39.00"
        },
        "Euro": {
            "buy": "38.00",
            "sale": "41.00"
        }
    }
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # second exec - no change
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('http://vkurse.dp.ua/course.json',)
    assert request_get_mock.call_args[1] == {}

    # third exec - change one rate
    response_json = {"Dollar": {"buy": "37.00", "sale": "39.00"}}
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json), )

    assert request_get_mock_2.call_count == 0
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1
