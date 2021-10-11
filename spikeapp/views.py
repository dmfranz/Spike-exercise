from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from spikeapp.models import Profile, RentalApplication, User
from django.http import HttpResponse, response
from .forms import CreateNewRentalApplication
from .forms import CreateRequestForm
from .forms import MakePayment, OwnerFeeForm
from .forms import RequestForm, ManageRequestForm
from spikeapp.cardhandling import TryPayment
from django.contrib import messages


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
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_number']
            f = RentalApplication(first_name=first_name, last_name=last_name, email=email, phone_number=phone_num)
            f.save()
        return redirect('../successful_application.html')
    else:
        form = CreateNewRentalApplication()
    
    return render(request, 'rental_application.html', {'form': form})


@login_required()
def dashboard(request):
    items = Profile.objects.filter(username=request.user)
    is_renter = items[0].is_renter
    balance = items[0].balance
    return render(request, 'dashboard.html', {'balance': balance, 'is_renter': is_renter})


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


@login_required()
def payment(request):
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
                curr_user.balance = curr_user.balance - final_form.Amount

                curr_user.save()
                final_form.save()
                messages.success(request, 'Payment successful!')
                return redirect('../dashboard')
            else:
                searched_user_objects = User.objects.filter(username=final_form.AffectedUser)
                if searched_user_objects.exists():

                    affected_user_object = searched_user_objects[0]

                    items = Profile.objects.filter(username=affected_user_object)
                    affected_user = items[0]
                    final_form.RunningBalance = affected_user.balance - final_form.Amount
                    affected_user.balance = final_form.RunningBalance

                    affected_user.save()
                    final_form.save()
                    messages.success(request, 'Payment successful!')
                    return redirect('../dashboard')
                else:
                    # This will be reached if the specified username was not found.
                    messages.error(request, 'Username not found, please try again.')
                    return redirect('.')
        else:
            messages.error(request, 'Payment failed, please ensure that fields are filled out correctly.')
            return redirect('.')
    else:
        payment_form = MakePayment()

    return render(request, 'payment.html', {'form': payment_form, 'is_tenant': is_tenant})

@login_required()
def fee(request):
    curr_user_query = Profile.objects.filter(username=request.user)
    curr_user = curr_user_query[0]
    is_tenant = curr_user.is_renter

    if request.method == "POST":
        fee_form = OwnerFeeForm(request.POST)

        if fee_form.is_valid() and not is_tenant:
            # final_form is the version of the form that will actually be saved to the database,
            # with fields modified as necessary
            final_form = fee_form.save(commit=False)
            fee_form.CreatingUser = curr_user.username

            # Need to set running balance, modify the user's balance, and set the affected user
            searched_user_objects = User.objects.filter(username=final_form.AffectedUser)
            # Need to confirm that the selected user account exists.
            if searched_user_objects.exists():
                affected_user_object = searched_user_objects[0]
                items = Profile.objects.filter(username=affected_user_object)
                affected_user = items[0]

                final_form.RunningBalance = affected_user.balance + final_form.Amount
                affected_user.balance = final_form.RunningBalance

                affected_user.save()
                final_form.save()
                return redirect('../dashboard')
            else:
                # This will be reached if the specified username was not found.
                return redirect('.')
        else:
            return redirect('.')
    else:
        fee_form = OwnerFeeForm()

    return render(request, 'fee.html', {'form': fee_form, 'is_tenant': is_tenant})


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
