from django.urls import path
from Post.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]