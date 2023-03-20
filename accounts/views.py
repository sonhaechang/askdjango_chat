from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render


# Create your views here.
login = LoginView.as_view(
    template_name = 'accounts/container/login.html',
    extra_context = {
        'form_name': '로그인',
        'submit_label': '로그인',
    }
)

logout = LogoutView.as_view(
    next_page = 'accounts:login'
)