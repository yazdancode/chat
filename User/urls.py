from django.urls import path

from User.views import ProfileView, ProfileEditView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit", ProfileEditView.as_view(), name="profile-edit"),
]
