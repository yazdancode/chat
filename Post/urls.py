from django.urls import path

from Post.views import HomeView, PostCreateView, post_delete_view

# from Post.views import home_view


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/delete/<pk>/", post_delete_view, name="post-delete"),
]
