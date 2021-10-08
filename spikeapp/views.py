from django.shortcuts import render, redirect
from spikeapp.models import Login
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
from .forms import CreateRequestForm
from .forms import MakePayment
from spikeapp.cardhandling import TryPayment
from spikeapp.models import User
# Create your views here.


def spikeapp(request):
    # logins = Login.objects.all()
    # context = {
    #     'logins': logins
    # }
    return render(request, 'home_page.html')


def rental_application(request):
    if request.method == "POST":
        form = CreateNewRentalApplication(request.POST)
        if form.is_valid():
            form.save()
        return redirect('..')
    else:
        form = CreateNewRentalApplication()
    
    return render(request, 'rental_application.html', {'form': form})


def dashboard(request):
    is_tenant = True
    return render(request, 'dashboard.html', {'is_tenant': is_tenant})


def requests(request):
    is_tenant = True
    if request.method == "POST":
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('..')
    else:
        form = CreateRequestForm()
    
    return render(request, 'requests.html', {'form':form, 'is_tenant': is_tenant})


def payment(request):
    if request.method == "POST":
        PaymentForm = MakePayment(request.POST)
        if PaymentForm.is_valid() and TryPayment(PaymentForm):
            PaymentForm.save()
            return redirect('../dashboard')
        else:
            return redirect('.')
    else:
        PaymentForm = MakePayment()

    return render(request, 'payment.html', {'form': PaymentForm})
