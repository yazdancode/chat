from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView

from User.models import Profile

from .forms import UserForm


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")

        if username:
            return get_object_or_404(Profile, user__username=username)
        elif self.request.user.is_authenticated:
            return self.request.user.profile
        else:
            raise Http404("User not found")


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.request.user.username})


class ProfileDeleteView(TemplateView):
    template_name = "users/profile_delete.html"
