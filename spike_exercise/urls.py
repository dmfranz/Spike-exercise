"""spike_exercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as v
from spikeapp import views as spikeapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name="register"),
    path('dashboard/', spikeapp_views.dashboard, name="dashboard"),
    path('payment/', spikeapp_views.payment, name="payment"),
    path('fees/', spikeapp_views.fee, name="fee"),
    path('', include('spikeapp.urls')),
    path('requests/', spikeapp_views.requests, name="requests"),
    path('', include('django.contrib.auth.urls')),
    path('rentalapplication/', spikeapp_views.rental_application, name="rental_application"),
    path('', include('django.contrib.auth.urls')),
    path('logout', v.logout_function, name="logout"),  # logout button pressed; called from form.
    path('manage_requests/', spikeapp_views.manage_requests, name='manage_requests'),
    path('view_requests/', spikeapp_views.view_requests, name='view_requests'),
    path('successful_application.html', spikeapp_views.successful_app, name="successful_application")
]
