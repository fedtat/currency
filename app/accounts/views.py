from accounts.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class MyProfile(LoginRequiredMixin, UpdateView):
    model = User  # the same as: queryset = User.objects.all()
    template_name = 'my_profile.html'
    success_url = reverse_lazy('index')
    fields = (
        'first_name',
        'last_name',
    )

    def get_object(self, queryset=None):
        return self.request.user

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # queryset = User.objects.all()  # the same as the row above
    #     queryset = queryset.filter(id=self.request.user.id)
    #     return queryset


class PasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User  # the same as: queryset = User.objects.all()
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')
    fields = (
        'password',
    )

    def get_object(self, queryset=None):
        return self.request.user
