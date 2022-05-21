from currency.filters import RateFilter
from currency.forms import ContactUsForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source
from currency.tasks import contact_us_async

from django.conf import settings  # if anything required from settings (NEVER DO THIS: from settings import settings!)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http.request import QueryDict
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from django_filters.views import FilterView


class ContactUsList(ListView):
    queryset = ContactUs.objects.all().order_by('-id')  # the same as this: model = ContactUs
    template_name = 'contactus_list.html'


class ContactUsCreate(LoginRequiredMixin, CreateView):
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
        data = form.cleaned_data
        contact_us_async.delay(
            data['subject'],
            data['email_from'],
            data['message']
        )
        self._send_email()
        return redirect


class RateList(FilterView):
    queryset = Rate.objects.all().order_by('-id').select_related('source')  # the same as this: model = Rate
    template_name = 'rate_list.html'
    paginate_by = 10
    filterset_class = RateFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        query_params = QueryDict(mutable=True)
        for key, value in self.request.GET.items():
            if key != 'page':
                query_params[key] = value

        context['filter_params'] = query_params.urlencode()
        return context


class RateCreate(CreateView):
    model = Rate
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateUpdate(UserPassesTestMixin, UpdateView):
    model = Rate
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser


class RateDelete(DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')


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


# class RateListApiExample(View):
#     def get(self, request):
#         import json
#         rates = Rate.objects.all()
#         rates_response = []
#         for rate in rates:
#             obj_dict = {
#                 'id': rate.id,
#                 'buy': str(rate.buy),
#                 'sale': str(rate.sale),
#             }
#             rates_response.append(obj_dict)
#         return HttpResponse(json.dumps(rates_response), content_type='application/json')

#
# class ExampleView(View):
#     def get(self, request):
#         from django.http import HttpResponse
#         from django.contrib.sessions.models import Session
#         from django.contrib.auth.models import User
#
#         session_id = request.COOKIES.get('sessionid')
#         if session_id:
#             print('SessionID is present:', session_id)
#
#             try:
#                 session_obj = Session.objects.get(session_key=session_id)  # block where an error is expected
#             except Session.DoesNotExist:
#                 print('Session not found')  # error interception if it occurs in "try" block
#             else:
#                 print(f'Session found:', session_obj)  # works only in case there were no errors in "try" block
#                 user_id = session_obj.get_decoded().get('_auth_user_id')
#                 try:
#                     user = User.objects.get(id=user_id)
#                 except User.DoesNotExist:
#                     print('User Not Found')
#                 else:
#                     print(f'Request user email is', user.email)
#                     print(f'Request user email is', request.user.email)
#             finally:
#                 pass  # works in any case
#
#         else:
#             print('Is not authenticated')
#
#         if request.user.is_authenticated:
#             if request.COOKIES.get('example_page_visited'):
#                 return HttpResponse('Already visited')
#             else:
#                 response = HttpResponse('First visit')
#                 response.set_cookie('example_page_visited', True)
#                 return response
#         else:
#             return HttpResponse('Please log in.')
