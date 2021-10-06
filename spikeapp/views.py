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
