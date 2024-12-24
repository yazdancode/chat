from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", blank=True, null=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True, unique=True)
    location = models.CharField(null=True, max_length=500, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self)-> str:
        return self.user.username

    def save(self, *args, **kwargs)-> None:
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        elif self.username:
            self.username = self.username.strip().lower()
        super().save(*args, **kwargs)

    @property
    def avatar(self)-> str:
        try:
            avatar = self.image.url
        except AttributeError:
            avatar = static("images/avatar_default.svg")
        return avatar

    @property
    def name(self)-> str:
        if self.username:
            name = self.username
        else:
            name = self.user.username
        return name
