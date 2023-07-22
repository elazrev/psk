from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.core.files.storage import default_storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invitations_received')
    is_manager = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if self.pk:
            # Retrieve existing instance from the database
            old_instance = Profile.objects.get(pk=self.pk)

            # Check if a new image is being uploaded
            if self.image != old_instance.image:
                # Delete the old image file from the media directory if it's not the default image
                if old_instance.image.name != 'default.png':
                    old_image_path = old_instance.image.path
                    if default_storage.exists(old_image_path):
                        default_storage.delete(old_image_path)

        # Save the instance
        super().save(*args, **kwargs)

        # Resize and save the image if necessary
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

