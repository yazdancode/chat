import uuid
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    image = models.URLField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    body = models.TextField()
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True, through="LikedPost"
    )
    dislikes = models.ManyToManyField(
        User, related_name="disliked_posts", blank=True, through="DisLikedPost"
    )
    tags = models.ManyToManyField("Tag", related_name="tagged_posts")
    created = models.DateTimeField(auto_now_add=True, db_index=True)
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


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title[:30]}"


# TODO : View this is not fixed
class DisLikedPost(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="dislike_posts"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_dislikes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} disliked {self.post.title[:30]}"


class LikedComment(models.Model):
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="liked_comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_likes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.comment.body[:30]}"


# TODO : View this is not fixed
class DisLikedComment(models.Model):
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="disliked_comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_dislikes"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} disliked {self.comment.body[:30]}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


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
    dislikes = models.ManyToManyField(
        User, related_name="disliked_comments", through="DisLikedComment"
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField()
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
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        User, related_name="liked_replies", through="LikedReply"
    )
    dislikes = models.ManyToManyField(
        User, related_name="disliked_replies", through="DisLikedReply"
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
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


class LikedReply(models.Model):
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE, related_name="liked_replies"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_liked_replies"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.reply.body[:30]}"


class DisLikedReply(models.Model):
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE, related_name="disliked_replies"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_disliked_replies"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} disliked {self.reply.body[:30]}"
