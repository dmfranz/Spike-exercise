from django.shortcuts import render, redirect
from spikeapp.models import Login
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
from .forms import MakePayment
from spikeapp.cardhandling import TryPayment
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
    
    return render(request, 'rental_application.html', {'form':form})


def dashboard(request):
    is_tenant = False
    return render(request, 'dashboard.html', {'is_tenant': is_tenant})


def payment(request):
    is_tenant = True

    if request.method == "POST":
        PaymentForm = MakePayment(request.POST)

        if PaymentForm.is_valid() and TryPayment(PaymentForm):
            # FinalForm is the version of the form that will actually be saved to the database,
            # with fields modified as necessary (based on tenant vs owner)
            FinalForm = PaymentForm.save(commit=False)

            FinalForm.ByTenant = is_tenant
            if FinalForm.ByTenant:
                FinalForm.DepositingUser = 'currentuser'
                FinalForm.AffectedUser = 'currentuser'
            else:
                FinalForm.DepositingUser = 'currentuser'
                FinalForm.AffectedUser = 'selecteduser'

            # Need to deduct paid amount from user account, or if owner, select account to be paying for
            # Also need to save running balance
            FinalForm.save()
            return redirect('../dashboard')
        else:
            return redirect('.')
    else:
        PaymentForm = MakePayment()

    return render(request, 'payment.html', {'form': PaymentForm, 'is_tenant': is_tenant})
