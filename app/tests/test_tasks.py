from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_privatbank


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
    assert request_get_mock.call_args[0] == ('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11', )
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
