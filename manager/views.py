from django.shortcuts import render, redirect
from .forms import InvitationForm
from .utils import generate_invitee_code
from django.views.generic import ListView
from .models import Invitation
from django.contrib import messages
from users.models import Profile


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

#customers page

class InvitedCustomersListView(ListView):
    model = Profile
    template_name = 'manager/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10  # Number of profiles to show per page

    def get_queryset(self):
        # Base queryset
        queryset = Profile.objects.filter(invited_by=self.request.user)

        # Sorting options
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'date_added':
            queryset = queryset.order_by('user__date_joined')
        elif sort_by == 'role':
            queryset = queryset.order_by('is_manager', 'is_patient')
        elif sort_by == 'first_name':
            queryset = queryset.order_by('user__first_name')
        elif sort_by == 'last_name':
            queryset = queryset.order_by('user__last_name')

        # Filtering options
        show_patients = self.request.GET.get('show_patients')
        show_managers = self.request.GET.get('show_managers')
        
        if show_patients:
            queryset = queryset.filter(is_patient=True)
        if show_managers:
            queryset = queryset.filter(is_manager=True)

        return queryset


            

