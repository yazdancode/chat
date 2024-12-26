import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Post.form import CommentCreateForm, PostCreateForm, PostEditForm, ReplyCreateForm
from Post.models import Comment, Like, Post, Reply, Tag


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


class PostPageView(DetailView):
    model = Post
    template_name = "posts/post_page.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commentform"] = CommentCreateForm()
        context["replyform"] = ReplyCreateForm()
        return context

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.object = self.get_object()
            if "top" in request.GET:
                comments = (
                    self.object.comments.annotate(num_likes=Count("likes"))
                    .filter(num_likes__gt=0)
                    .order_by("-num_likes")
                )
            else:
                comments = self.object.comments.all()
            return render(
                request,
                "snippets/loop_postpage_comments.html",
                {"comments": comments, "replyform": ReplyCreateForm()},
            )
        return super().get(request, *args, **kwargs)


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


def like_post(request, pk) -> None:
    post = get_object_or_404(Post, id=pk)
    like_exists = Like.objects.filter(
        username=request.user.username, post=post
    ).exists()

    if post.author != request.user:
        if like_exists:
            Like.objects.filter(user=request.user, post=post).delete()
        else:
            Like.objects.create(user=request.user, post=post)
    return render(request, "snippets/like.html", {"post": post})
