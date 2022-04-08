from currency.forms import ContactUsForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.conf import settings  # if anything required from settings (NEVER DO THIS: from settings import settings!)
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ContactUsList(ListView):
    queryset = ContactUs.objects.all().order_by('-id')  # the same as this: model = ContactUs
    template_name = 'contactus_list.html'


class ContactUsCreate(CreateView):
    model = ContactUs
    template_name = 'contactus_create.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('index')

    def _send_email(self):
        # recipient = settings.EMAIL_HOST_USER
        subject = 'User ContactUs'
        body = f'''
            Request From: {self.object.name}
            Email to reply: {self.object.email_from}
            Subject: {self.object.subject}
            Body: {self.object.message}
        '''
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_email()
        return redirect


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
