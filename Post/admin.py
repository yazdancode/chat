from django.contrib import admin

from Post.models import Comment, LikePost, Post, Reply, Tag, LikedComment

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikePost)
admin.site.register(LikedComment)
