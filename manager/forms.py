from django import forms
from .models import Invitation

class InvitationForm(forms.ModelForm):
    
    is_manager = forms.BooleanField(required=False)  # Add the is_manager field
    is_patient = forms.BooleanField(required=False)  # Add the is_patient field

    class Meta:
        model = Invitation
        fields = ['invitee_email', 'is_manager', 'is_patient']
