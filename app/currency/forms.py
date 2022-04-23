from currency.models import ContactUs, Rate, Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'code_name', 'source_url', 'phone')


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email_from', 'subject', 'message')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('base_type', 'type', 'source', 'buy', 'sale')
