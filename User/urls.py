from django.urls import path
from .views import ProfileView, ProfileEditView

urlpatterns = [
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
]
