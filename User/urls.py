from django.urls import path

from .views import ProfileDeleteView, ProfileEditView, ProfileView

urlpatterns = [
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile-delete"),
]
