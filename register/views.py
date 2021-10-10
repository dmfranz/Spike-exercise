from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from spikeapp.forms import ProfileForm


def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile.fullname = profile_form.cleaned_data.get('fullname')
            user.profile.is_renter = profile_form.cleaned_data.get('is_renter')
            user.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return redirect('/dashboard')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'register/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def logout_function(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
