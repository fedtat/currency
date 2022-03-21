from currency.forms import SourceForm
from currency.models import ContactUs, Rate, Source

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ContactsList(ListView):
    queryset = ContactUs.objects.all().order_by('-id')  # the same as this: model = ContactUs
    template_name = 'contacts_list.html'


class RateList(ListView):
    queryset = Rate.objects.all().order_by('-id')  # the same as this: model = Rate
    template_name = 'rate_list.html'


class SourceList(ListView):
    model = Source
    template_name = 'source_list.html'


class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'


class SourceCreate(CreateView):
    model = Source
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceUpdate(UpdateView):
    model = Source
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceDelete(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')
