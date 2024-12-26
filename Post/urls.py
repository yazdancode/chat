from django.urls import path

from Post.views import (
    CommentDeleteView,
    CommentSentView,
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostEditView,
    PostPageView,
    ReplyDeleteView,
    ReplySentView,
    LikePostView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("tag/<slug:tag>/", HomeView.as_view(), name="home_by_tag"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/edit/", PostEditView.as_view(), name="post-edit"),
    path("post/<int:pk>/", PostPageView.as_view(), name="post-page"),
    path("post/<int:pk>/add_comment/", CommentSentView.as_view(), name="comment-sent"),
    path("comment/<int:pk>/add_reply/", ReplySentView.as_view(), name="reply-sent"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
    path("reply/<int:pk>/delete/", ReplyDeleteView.as_view(), name="reply-delete"),
    path("post/<int:pk>/like/", LikePostView, name="like-post"),
    path("comment/<int:pk>/like/", like_comment, name="like-comment"),
]
