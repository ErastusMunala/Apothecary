from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def sales(request):
    return HttpResponse("Sales")
def products(request):
   return render(request, 'products.html')
def pharmacy(request):
    return render(request, 'pharmacy.html')
def home(request):
    return render(request, 'index.html')
# Create your views here.
def original(request):
    return render(request, 'original.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')