from django.contrib import admin

from Post.models import Comment, LikedComment, LikedPost, Post, Reply, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
