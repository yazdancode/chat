from django.urls import path

from Post.views import (
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostEditView,
    PostDetailView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/delete/<pk>/", PostDeleteView.as_view(), name="post-delete"),
    path("post/edit/<pk>/", PostEditView.as_view(), name="post-edit"),
    path("post/<pk>/", PostDetailView.as_view(), name="post-detail"),
]
