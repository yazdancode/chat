import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Post.base import (
    DisLikedCommentToggleView,
    DisLikedReplyToggleView,
    DisLikeToggleView,
    LikedCommentToggleView,
    LikedReplyToggleView,
    LikeToggleView,
)
from Post.forms import CommentCreateForm, PostCreateForm, PostEditForm, ReplyCreateForm
from Post.models import Comment, Post, Reply, Tag


class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag")
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            return Post.objects.filter(tags__slug=tag_slug)
        self.tag = None
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create_view.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        try:
            website = requests.get(form.cleaned_data["url"])
            sourcecode = BeautifulSoup(website.text, "html.parser")
        except Exception as e:
            messages.error(self.request, f"Error fetching the website: {e}")
            return redirect("post-create")
        find_image = sourcecode.select(
            'meta[content^="https://live.staticflickr.com/"]'
        )
        try:
            image = find_image[0]["content"]
        except IndexError:
            messages.error(self.request, "Requested image is not on Flickr!")
            return redirect("post-create")
        post.image = image
        find_title = sourcecode.select("h1.photo-title")
        if find_title:
            post.title = find_title[0].text.strip()
        find_artist = sourcecode.select("a.owner-name")
        if find_artist:
            post.artist = find_artist[0].text.strip()
        post.author = self.request.user
        post.save()
        form.save_m2m()
        return redirect("home")

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
        )
        return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error updating the post. Please try again."
        )
        return super().form_invalid(form)


class PostPageView(View):
    template_name = "a_posts/post_page.html"
    htmx_template_name = "snippets/loop_postpage_comments.html"

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        commentform = CommentCreateForm()
        replyform = ReplyCreateForm()

        if request.htmx:
            comments = self.get_comments(request, post)
            return render(
                request,
                self.htmx_template_name,
                {"comments": comments, "replyform": replyform},
            )

        context = {
            "post": post,
            "commentform": commentform,
            "replyform": replyform,
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_comments(request, post):
        if "top" in request.GET:
            return (
                post.comments.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )
        return post.comments.all()


class CommentSentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "snippets/add_comment.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.parent_post = post
        comment.save()
        replyform = ReplyCreateForm()
        context = {
            "post": post,
            "comment": comment,
            "replyform": replyform,
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        replyform = ReplyCreateForm()
        context = {
            "post": post,
            "form": form,
            "replyform": replyform,
        }
        return render(self.request, self.template_name, context)


class ReplySentView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyCreateForm
    template_name = "snippets/add_reply.html"

    def form_valid(self, form):
        comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.parent_comment = comment
        reply.save()
        context = {
            "reply": reply,
            "comment": comment,
            "replyform": ReplyCreateForm(),
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        context = {
            "form": form,
            "comment": comment,
            "replyform": form,
        }
        return render(self.request, self.template_name, context)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_delete.html"
    context_object_name = "comment"

    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs["pk"], author=self.request.user)

    def get_success_url(self):
        comment = self.get_object()
        messages.success(self.request, "Comment deleted")
        return reverse_lazy("post", kwargs={"pk": comment.parent_post.id})


class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = "posts/reply_delete.html"
    context_object_name = "reply"

    def get_queryset(self):
        return Reply.objects.filter(id=self.kwargs["pk"], author=self.request.user)

    def get_success_url(self):
        reply = self.get_object()
        messages.success(self.request, "Reply deleted")
        return reverse_lazy("post", kwargs={"pk": reply.parent_comment.parent_post.id})

    def form_valid(self, form):
        return super().form_valid(form)


class LikePostView(LikeToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/likes_post.html"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get("post_id"))
        response = super().post(request, post_id=kwargs.get("post_id"))
        if not request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, self.template_name, {"post": post})
        return response


# TODO : file html this is not fixed
class DisLikePostView(DisLikeToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/dislikes_post.html"

    def post(self, request, *args, **kwargs):
        kwargs["model"] = Post
        response = super().post(request, *args, **kwargs)
        if not request.is_ajax():
            instance = get_object_or_404(Post, id=kwargs.get("pk"))
            return render(request, self.template_name, {"post": instance})
        return response


class LikeCommentView(LikedCommentToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/likes_comment.html"

    def post(self, request, *args, **kwargs):
        kwargs["model"] = Comment
        response = super().post(request, *args, **kwargs)
        if not request.is_ajax():
            instance = get_object_or_404(Comment, id=kwargs.get("pk"))
            return render(request, self.template_name, {"comment": instance})
        return response


# TODO : file html this is not fixed
class DisLikeCommentView(DisLikedCommentToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/dislikes_comment.html"

    def post(self, request, *args, **kwargs):
        kwargs["model"] = Comment
        response = super().post(request, *args, **kwargs)
        if not request.is_ajax():
            instance = get_object_or_404(Comment, id=kwargs.get("pk"))
            return render(request, self.template_name, {"comment": instance})
        return response


class LikeReplyView(LikedReplyToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/likes_reply.html"

    def post(self, request, *args, **kwargs):
        kwargs["model"] = Reply
        response = super().post(request, *args, **kwargs)
        if not request.is_ajax():
            instance = get_object_or_404(Reply, id=kwargs.get("pk"))
            return render(request, self.template_name, {"reply": instance})
        return response


# TODO : file dislikes_reply.html this is not fixed
class DisLikeReplyView(DisLikedReplyToggleView, LoginRequiredMixin, ListView):
    template_name = "snippets/dislikes_reply.html"

    def post(self, request, *args, **kwargs):
        kwargs["model"] = Reply
        response = super().post(request, *args, **kwargs)
        if not request.is_ajax():
            instance = get_object_or_404(Reply, id=kwargs.get("pk"))
            return render(request, self.template_name, {"reply": instance})
        return response
