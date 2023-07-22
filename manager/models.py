from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_invitee_code

class Invitation(models.Model):
    invitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_sent')
    invitee_email = models.EmailField()
    invitee_code = models.CharField(max_length=50, unique=True)
    is_manager = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    invitation_status = models.CharField(max_length=20, choices=(('waiting', 'בהמתנה'), ('approved', 'בוצע')), default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['invitor', 'invitee_code']

    def __str__(self):
        return self.invitee_email

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.invitor_id:
                # Set the invitor as the user who initiated the invitation
                user = kwargs.get('user')
                if user:
                    self.invitor = user

            self.invitee_code = generate_invitee_code()

        super().save(*args, **kwargs)

    
            

