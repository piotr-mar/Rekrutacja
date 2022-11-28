from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class UserLogin(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully login.")
            return redirect("main")
        messages.error(request, "Wrong username or password")
        return redirect("login")


class UserLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logout")
        return redirect("main")


class UseRegister(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully register and login")
            return redirect("main")
        messages.error(request, "Invalid data")
        return redirect('register')