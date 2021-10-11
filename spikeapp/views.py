from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from spikeapp.models import Profile, User
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
from .forms import CreateRequestForm
from .forms import MakePayment
from .forms import RequestForm, ManageRequestForm
from spikeapp.cardhandling import TryPayment


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


@login_required()
def dashboard(request):
    items = Profile.objects.filter(username=request.user)
    is_renter = items[0].is_renter
    return render(request, 'dashboard.html', {'is_renter': is_renter})


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


def manage_requests(request):
    query_results = RequestForm.objects.filter(landlord_name=str(request.user).lower().strip())
    # print(request.user) the username of current user + RequestForm.landlord_name must be equal
    # query_results = RequestForm.objects.all()
    form = ManageRequestForm(request.POST)
    if form.is_valid():
        # response = form.get('response')
        # form.update(response=response)
        form.save()
        return redirect('..')

    return render(request, 'manage_requests.html', {'form': form, 'query_results': query_results})


def view_requests(request):
    query_results = RequestForm.objects.filter(tenant_name=str(request.user).lower().strip())
    # print(request.user) the username of current user + RequestForm.landlord_name must be equal
    # query_results = RequestForm.objects.all()

    form = ManageRequestForm(request.GET)
    if form.is_valid():
        form.save()
        return redirect('../view_requests')

    #Don't we need a from variable here to be able to see the new data?

    return render(request, 'view_requests.html', {'form': form, 'query_results': query_results})
