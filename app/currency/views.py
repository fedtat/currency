import random
import string

from currency.forms import SourceForm
from currency.models import ContactUs, Rate, Source

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

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


def source_list(request):
    sources = Source.objects.all().order_by('-id')
    return render(request, 'source_list.html', context={'sources': sources})


def source_create(request):
    if request.method == 'POST':  # validate user data
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    else:  # get empty form
        form = SourceForm()

    return render(request, 'source_create.html', context={'form': form})


def source_update(request, pk):
    # try:
    #     instance = Source.objects.get(pk=pk)
    # except Source.DoesNotExist:
    #     raise Http404(f'Object does not exist')
    instance = get_object_or_404(Source, pk=pk)

    if request.method == 'POST':  # validate user data
        form = SourceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    else:  # get empty form
        form = SourceForm(instance=instance)

    return render(request, 'source_update.html', context={'form': form})


def source_delete(request, pk):
    instance = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect('/source/list/')
    else:
        return render(request, 'source_delete.html', context={'source': instance})


def index(request):
    return render(request, 'index.html')
