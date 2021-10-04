from django.shortcuts import render

# Create your views here.

def spikeapp(request):
    return render(request, 'helloworld.html',{})