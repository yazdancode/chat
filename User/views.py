from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView

from User.models import Profile

from User.forms import UserForm


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")

        if username:
            user = get_object_or_404(User, username=username)
            return user.profile
        else:
            return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse("profile-edit", kwargs={"username": self.request.user.username})


class ProfileDeleteView(DeleteView):
    model = User
    template_name = "users/profile_delete.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_success_url(self):
        return reverse_lazy("home")
