from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginRequiredMixin, LoginView):
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('scv-home')
