from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from spikeapp.forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {'form': form})


def logout_function(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
