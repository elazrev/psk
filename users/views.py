from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from manager.models import Invitation
from .models import Profile
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            invitation = Invitation.objects.filter(invitee_email=user.email, invitation_status='waiting').first()
            if invitation:
                user.is_active = True
                user.save()
                invitation.invitation_status = 'approved'
                invitation.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')



def direction_page(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile

        if user_profile.is_manager:
            return redirect(reverse('manager:manager-dashboard'))
        elif user_profile.is_patient:
            return redirect(reverse('patient:patient-dashboard'))

    # If the user is not authenticated or doesn't have a profile, redirect to a login page or homepage.
    # Example:
    return redirect('login')  # Replace 'home' with the name of your homepage URL pattern.