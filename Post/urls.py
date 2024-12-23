from django.urls import path

from Post.views import (
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostPageView,
    PostEditView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<tag>/", HomeView.as_view(), name="category-detail"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("post/delete/<pk>/", PostDeleteView.as_view(), name="post-delete"),
    path("post/edit/<pk>/", PostEditView.as_view(), name="post-edit"),
    path("post/<pk>/", PostPageView.as_view(), name="post-detail"),
]
