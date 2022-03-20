import random
import string

from currency.models import ContactUs, Rate

from django.http import HttpResponse
from django.shortcuts import render

from faker import Faker


def generate_users(users_count=10):
    """
    Generates random users with a name and email.
    :param users_count: number of users that should be generated
    :return: strings of randomly generated user name and email
    """
    fake = Faker()
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    domains = ["org", "net", "com", "ua"]
    result = ""
    for _ in range(users_count):
        random_string = "".join(random.choice(chars) for _ in range(random.randint(5, 10)))
        result += f"{fake.name().split()[0]} {random_string}@mail.{random.choice(domains)} \n"
    return result


def hello_world(request):
    default_count = 10
    if 'count' in request.GET:
        count = int(request.GET['count'])
    else:
        count = default_count
    if count > 1000:
        count = default_count
    return HttpResponse(generate_users(count))


def contacts_list(request):
    '''
    Get users' contacts data from the database
    :return: list of lists with users' emails and messages
    '''
    contacts = ContactUs.objects.all()
    return render(request, 'contacts_list.html', context={'contacts': contacts})


def rate_list(request):
    rates = Rate.objects.all()
    return render(request, 'rate_list.html', context={'rates': rates})


def index(request):
    return render(request, 'index.html')
