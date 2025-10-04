from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.models import User


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    success_url = reverse_lazy("cash_flow:home_page")


def logout_view(request):
    logout(request)
    return redirect("/")
