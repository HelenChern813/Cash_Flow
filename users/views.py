from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CustomUserCreationForm
from users.models import User


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")
    form_class = CustomUserCreationForm


def logout_view(request):
    logout(request)
    return redirect("/")
