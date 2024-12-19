from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", blank=True, null=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True, unique=True)
    location = models.CharField(null=True, max_length=500, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        if self.username:
            self.username = self.username.strip().lower()

        super().save(*args, **kwargs)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar_default.svg")
        return avatar

    @property
    def name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
