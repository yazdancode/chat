from django.urls import path

from .views import (
    ProfileDeleteView,
    ProfileEditView,
    ProfileView,
    ProfileOnboardingView,
)

urlpatterns = [
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path(
        "profile/edit/<str:username>/", ProfileEditView.as_view(), name="profile-edit"
    ),
    path(
        "profile/delete/<str:username>/",
        ProfileDeleteView.as_view(),
        name="profile_delete",
    ),
    path(
        "profile/onboarding/",
        ProfileOnboardingView.as_view(),
        name="profile_onboarding",
    ),
]
