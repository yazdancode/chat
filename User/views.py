from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import UpdateView

# from inbox.forms import InboxNewMessageForm
from Post.forms import InboxNewMessageForm, ReplyCreateForm
from User.forms import UserForm
from User.models import Profile, User


class ProfileView(View):
    template_name = "users/profile.html"

    def get(self, request, username=None):
        if username:
            profile = get_object_or_404(User, username=username).profile
        else:
            try:
                profile = request.user.profile
            except AttributeError:
                raise Http404()

        posts = profile.user.posts.all()

        if request.htmx:
            return self.handle_htmx_requests(request, profile)

        new_message_form = InboxNewMessageForm()

        context = {
            "profile": profile,
            "posts": posts,
            "new_message_form": new_message_form,
        }

        return render(request, self.template_name, context)

    @staticmethod
    def handle_htmx_requests(request, profile):
        if "top-posts" in request.GET:
            posts = (
                profile.user.posts.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )
        elif "top-comments" in request.GET:
            comments = (
                profile.user.comments.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )
            replyform = ReplyCreateForm()
            return render(
                request,
                "snippets/loop_profile_comments.html",
                {"comments": comments, "replyform": replyform},
            )
        elif "liked-posts" in request.GET:
            posts = profile.user.likedposts.order_by("-likedpost__created")
        else:
            posts = profile.user.posts.all()

        return render(request, "snippets/loop_profile_posts.html", {"posts": posts})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileDeleteView(LoginRequiredMixin, View):
    template_name = "users/profile_delete.html"

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity")
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProfileVerifyEmailView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        send_email_confirmation(request, request.user)
        return redirect("profile")
