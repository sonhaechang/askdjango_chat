from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


# Create your views here.
login = LoginView.as_view(
    template_name = 'accounts/container/login.html',
    extra_context = {
        'form_name': 'Login',
        'submit_label': 'Login',
    }
)


logout = LogoutView.as_view(
    next_page = 'accounts:login'
)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/container/profile.html'


signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name = 'accounts/container/signup.html',
    extra_context = {
        'form_name': 'Signup',
        'submit_label': 'Signup',
    },
    success_url = reverse_lazy('accounts:login')
)