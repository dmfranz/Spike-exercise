from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from spikeapp.models import Profile, RentalApplication, User
from django.http import HttpResponse, response, HttpResponseRedirect
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
            landlord = form.cleaned_data['landlord']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_number']
            f = RentalApplication(landlord=landlord, first_name=first_name, last_name=last_name, email=email, phone_number=phone_num)
            f.save()
        return redirect('../successful_application.html')
    else:
        form = CreateNewRentalApplication()
    
    return render(request, 'rental_application.html', {'form': form})


def view_applications(request):
    items = RentalApplication.objects.filter(landlord=request.user)
    return render(request, 'view_applications.html', {'items': items})


def accept_application(request):
    items = RentalApplication.objects.filter(id=request.POST['Accept'])
    item = items[0]
    item.status = "Accepted"
    item.save()
    return HttpResponseRedirect('/view_applications/')


def reject_application(request):
    items = RentalApplication.objects.filter(id=request.POST['Reject'])
    item = items[0]
    item.status = "Rejected"
    item.save()
    return HttpResponseRedirect('/view_applications/')


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


def successful_app(request):
    return render(request, 'successful_application.html')