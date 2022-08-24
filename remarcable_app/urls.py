
from django.urls import path
from remarcable_app import views

urlpatterns = [
    path('',views.home,name='home'),
    
]