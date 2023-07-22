from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'patient'

urlpatterns = [
    path('', views.home, name='patient-dashboard'),
    
]
