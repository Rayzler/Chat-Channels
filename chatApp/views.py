from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import SignUpForm


# Create your views here.
def frontpage(request):
    return render(request, "chatApp/frontpage.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("frontpage")
    else:
        form = SignUpForm()

    return render(request, "chatApp/signup.html", {"form": form})


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('frontpage')
        else:
            return render(request, 'chatApp/login.html', {'error_message': 'Credenciales inválidas'})

    return render(request, "chatApp/login.html")


def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy("login"))
