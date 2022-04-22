from accounts.models import User
from accounts.tasks import send_activation_email

from django import forms


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

        send_activation_email.delay()

        return user
