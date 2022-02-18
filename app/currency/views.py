import random
import string

from django.http import HttpResponse

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
    if 'count' in request.GET:
        count = int(request.GET['count'])
        return HttpResponse(generate_users(count))
    else:
        return HttpResponse(generate_users())
