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
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True, through="LikePost"
    )
    tags = models.ManyToManyField("Tag", related_name="tagged_posts")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created"]


class LikePost(models.Model):
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="like_posts"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.comment.body[:30]}"


class LikedComment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked_comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_likes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["order"]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    parent_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        User, related_name="liked_comments", through="LikedComment"
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    def __str__(self) -> str:
        return (
            f"{self.author.username if self.author else 'no author'} : {self.body[:30]}"
        )

    class Meta:
        ordering = ["-created"]


class Reply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="replies"
    )
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    def __str__(self) -> str:
        return (
            f"{self.author.username if self.author else 'no author'} : {self.body[:30]}"
        )

    class Meta:
        ordering = ["-created"]
