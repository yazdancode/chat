import uuid

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    body = models.TextField()
    tags = models.ManyToManyField("Tag")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        max_length=100,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
