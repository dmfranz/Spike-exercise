from django.shortcuts import render, redirect
from spikeapp.models import Login
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
# Create your views here.

def spikeapp(request):
    # logins = Login.objects.all()
    # context = {
    #     'logins': logins
    # }
    return render(request, 'spike_app_index.html')

def rental_application(request):
    if request.method == "POST":
        form = CreateNewRentalApplication(request.POST)
        if form.is_valid():
            form.save()
        return redirect('..')
    else:
        form = CreateNewRentalApplication()
    
    return render(request, 'rental_application.html', {'form':form})