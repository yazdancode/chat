from django.urls import path

from User.views import (
    ProfileDeleteView,
    ProfileEditView,
    ProfileVerifyEmailView,
    ProfileView,
)

urlpatterns = [
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("profile/", ProfileView.as_view(), name="my_profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    path(
        "profile/verify-email/",
        ProfileVerifyEmailView.as_view(),
        name="profile_verify_email",
    ),
]
