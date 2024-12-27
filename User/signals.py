from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        if not Profile.objects.filter(email=instance.email).exists():
            Profile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=Profile, dispatch_uid="update_profile_signal")
def update_profile(instance, created, **kwargs) -> None:
    if not created:
        try:
            user = instance.user
            if user.email != instance.email:
                user.email = instance.email
                user.save()
        except Exception as e:
            print(f"Error updating user email: {e}")
