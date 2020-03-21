from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def owhome(request):
    return render(request, 'owner/owhome.html')