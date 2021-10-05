from django.shortcuts import render
from spikeapp.models import Login
from django.http import HttpResponse, response
from .forms import CreateNewAccount
# Create your views here.

def spikeapp(request):
    logins = Login.objects.all()
    context = {
        'logins': logins
    }
    return render(request, 'spike_app_index.html',context=context)

# TODO
# 1) Check if this user already exists
# 2) Decide some action on failure
def createaccount(request):
    if request.method == "POST":
        form = CreateNewAccount(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            re_entered_password = form.cleaned_data['re_entered_pass']

            # Does nothing if the passwords dont match for the time being
            if password == re_entered_password:
                # encrypt the password here
                login = Login(username=username, password=password)
                login.save()

        return response.HttpResponseRedirect("..")
    else:
        form = CreateNewAccount()
    
    return render(request, "createaccount.html",{"form":form})