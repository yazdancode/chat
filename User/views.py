from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView
from User.forms import UserForm
from User.models import Profile
from django.contrib import messages


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")

        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user

        profile, created = Profile.objects.get_or_create(user=user)
        return profile


class ProfileEditView(UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse("profile-edit", kwargs={"username": self.request.user.username})


class ProfileOnboardingView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_onboarding.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/profile_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        if user != self.request.user:
            messages.error(self.request, "You cannot delete another user's account.")
            return redirect("home")
        return user

    def form_valid(self, form):
        messages.success(self.request, "Account deleted successfully")
        logout(self.request)
        return super().form_valid(form)
