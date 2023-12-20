from django.urls import path
from . import views

#URLConf modu
urlpatterns = [
    path('', views.home, name='home'),
    path('pharmacy/', views.pharmacy, name='pharmacy'),
    path('products/', views.products, name='products'),
    path('sales/', views.sales, name='sales'),
    path('original/', views.original, name='original'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]
