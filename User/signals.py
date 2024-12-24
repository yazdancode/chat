from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User, dispatch_uid="create_profile_signal")
def manage_profile(instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(user=user, email=user.email)
    else:
        try:
            profile = Profile.objects.get(user=user)
            profile.email = user.email
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, email=user.email)


@receiver(post_save, sender=Profile, dispatch_uid="update_profile_signal")
def update_profile(instance, created, **kwargs):
    if not created:
        try:
            user = instance.user
            if user.email != instance.email:
                user.email = instance.email
                user.save()
        except Exception as e:
            print(f"Error updating user email: {e}")
