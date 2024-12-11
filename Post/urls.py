from django.urls import path

from Post.views import HomeView, PostCreateView, PostDeleteView, PostUpdateView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/delete/<pk>/", PostDeleteView.as_view(), name="post-delete"),
    path("post/edit/<pk>/", PostUpdateView.as_view(), name="post-edit"),
]
