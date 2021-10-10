from django.urls import path
from spikeapp import views

urlpatterns = [
    path('', views.spikeapp, name='spikeapp'),
]
