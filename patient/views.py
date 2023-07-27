from django.shortcuts import render
from datetime import datetime

def home(request):
    # Replace dummy_date with the actual datetime for the treatment
    dummy_date = datetime(2023, 7, 31, 15, 30)  # For example, 31st July 2023, 15:30
    context = {
        "title": "Dashboard",
        "treatment_date": dummy_date,
    }
    return render(request, 'patient/home.html', context)
