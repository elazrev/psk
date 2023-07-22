from django.shortcuts import render

def home(request):
    context ={
        "title": "Dashboard",
    }
    return render(request, 'patient/home.html', context)

