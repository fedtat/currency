from accounts.models import User

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords should match.')

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        user = super().save(commit=False)
        user.set_password(cleaned_data['password1'])
        user.is_active = False

        if commit:
            user.save()

        self._send_activation_email(user)

        return user

    def _send_activation_email(self, user):

        subject = 'Sign Up'
        body = f'''
        Activation Link:
        {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate-user', args=[user.username])}
        '''
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject,
            body,
            email_from,
            [user.email],
            fail_silently=False
        )
