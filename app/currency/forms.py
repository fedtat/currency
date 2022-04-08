from currency.models import ContactUs, Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url', 'phone')


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'email_from', 'subject', 'message')
