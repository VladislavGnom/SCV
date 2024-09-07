from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginRequiredMixin, LoginView):
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('scv-home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "I want this on the template"
        context["example2"] = "I want this on the template too"
        return context