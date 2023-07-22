from django.shortcuts import render, redirect
from .forms import InvitationForm
from .utils import generate_invitee_code
from .models import Invitation
from django.contrib import messages


def home(request):
    context = {
        "title": "Dashboard",
    }
    return render(request, 'manager/home.html', context)


def invitations_view(request):
    invitations = Invitation.objects.all()
    return render(request, 'manager/invitations.html', {'invitations': invitations})


def send_invitation(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.invitor = request.user  # Set the invitor as the user who initiated the invitation
            invitation.invitee_code = generate_invitee_code()  # Implement the code to generate a unique invitee code

            # Check if the invitee email matches an existing invitation
            if Invitation.objects.filter(invitee_email=invitation.invitee_email).exists():
                messages.error(request, 'This email is already invited.')
                return redirect('manager:send-invitation')

            invitation.save()
            return redirect('manager:invitation-success')
    else:
        form = InvitationForm()

    return render(request, 'manager/send_invitation.html', {'form': form})


def delete_invitation(request, invitation_id):
    invitation = Invitation.objects.get(pk=invitation_id)
    invitation.delete()
    messages.success(request, 'Invitation deleted successfully.')
    return redirect('manager:invitations-view')
