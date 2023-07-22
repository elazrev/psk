from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from manager.models import Invitation


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        invitation = Invitation.objects.filter(invitee_email=instance.email).first()
        if invitation and invitation.invitor.profile:
            invitor_profile = invitation.invitor.profile
            if invitation.is_manager:
                profile.is_manager = True
            elif invitation.is_patient:
                profile.is_patient = True
            profile.invited_by = invitor_profile.user
            profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
