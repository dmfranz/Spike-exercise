from django.urls import path
from spikeapp import views

urlpatterns = [
    path('', views.spikeapp, name='spikeapp'),
    path('rental_appliaction',views.rental_application, name='rental_application'),
]