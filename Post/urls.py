from django.urls import path

from Post.views import HomeView

# from Post.views import home_view


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
