from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from User.models import Profile
from django.views.generic.edit import UpdateView
from .forms import UserForm
from django.urls import reverse


# TODO : function with test written There is no readability in the code at all
# def profile_view(request):
#     profile = request.user.profile
#     return render(request, "users/profile.html", {"profile": profile})


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self, **kwargs):
        return self.request.user.profile


# TODO : function with test written There is no readability in the code at all
# @login_required
# def profile_edit_view(request):
#     profile = request.user.profile
#     if request.method == "POST":
#         form = UserForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("profile"))
#     else:
#         form = UserForm(instance=profile)
#
#     return render(request, "users/profile_edit.html", {"form": form})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("profile")
