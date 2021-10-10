from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from spikeapp.models import Profile, User
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
from .forms import CreateRequestForm
from .forms import MakePayment
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
    print(is_renter)
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
    profiles = Profile.objects.all()
    curr_user_query = Profile.objects.filter(username=request.user)
    curr_user = curr_user_query[0]
    is_tenant = curr_user.is_renter

    if request.method == "POST":
        payment_form = MakePayment(request.POST)

        if payment_form.is_valid() and TryPayment(payment_form):
            # FinalForm is the version of the form that will actually be saved to the database,
            # with fields modified as necessary (based on tenant vs owner)
            final_form = payment_form.save(commit=False)

            final_form.ByTenant = is_tenant
            final_form.DepositingUser = curr_user.username

            # Exact functions are dependent on if this is a tenant or owner
            # Need to set running balance and modify the user's balance, and possibly set the affected user
            if final_form.ByTenant:
                final_form.AffectedUser = curr_user.username
                final_form.RunningBalance = curr_user.balance - final_form.Amount
                curr_user.balance = final_form.RunningBalance
            else:
                items = Profile.objects.filter(username=final_form.AffectedUser)
                affected_user = items[0]
                final_form.RunningBalance = affected_user.balance - final_form.Amount
                affected_user.balance = final_form.RunningBalance

            final_form.save()
            return redirect('../dashboard')
        else:
            return redirect('.')
    else:
        payment_form = MakePayment()

    return render(request, 'payment.html', {'form': payment_form, 'is_tenant': is_tenant})
