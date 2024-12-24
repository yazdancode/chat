from typing import Any, Optional

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from Post.form import CommentCreateForm, PostCreateForm, PostEditForm
from Post.models import Post, Tag


class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self)-> Any:
        tag_slug = self.kwargs.get("tag")
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            return Post.objects.filter(tags__slug=tag_slug)
        return Post.objects.all()

    def get_context_data(self, **kwargs)-> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Tag.objects.all()
        context["selected_tag"] = getattr(self, "tag", None)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create_view.html"

    def form_valid(self, form)-> Any:
        post = form.save(commit=False)
        try:
            metadata = self.fetch_metadata(form.cleaned_data["url"])
            post.image = metadata.get("image", "")
            post.title = metadata.get("title", "")
            post.artist = metadata.get("artist", "")
        except Exception as e:
            messages.error(self.request, f"خطایی هنگام پردازش لینک رخ داد: {str(e)}")
            return redirect("post_create")

        post.author = self.request.user
        post.save()
        form.save_m2m()
        messages.success(self.request, "پست با موفقیت ایجاد شد.")
        return redirect("home")

    @staticmethod
    def fetch_metadata(url: str) -> dict[str, Optional[str]]:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        source_code = BeautifulSoup(response.text, "html.parser")

        image_meta = source_code.select(
            'meta[content^="https://live.staticflickr.com/"]'
        )
        title_element = source_code.select("h1.photo-title")
        artist_element = source_code.select("a.owner-name")

        return {
            "image": image_meta[0]["content"] if image_meta else None,
            "title": title_element[0].text.strip() if title_element else None,
            "artist": artist_element[0].text.strip() if artist_element else None,
        }


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    context_object_name = "post"

    def get_object(self, queryset=None)-> Post:
        return get_object_or_404(Post, id=self.kwargs["pk"], author=self.request.user)

    def get_success_url(self)-> str:
        messages.success(self.request, "پست با موفقیت حذف شد.")
        return reverse_lazy("home")


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"

    def get_object(self, queryset=None)-> HttpResponseRedirect | Model | Any:
        post = super().get_object(queryset)
        if post.author != self.request.user:
            messages.error(self.request, "شما اجازه ویرایش این پست را ندارید.")
            return redirect("home")
        return post

    def form_valid(self, form)-> Any:
        response = super().form_valid(form)
        messages.success(self.request, "پست با موفقیت ویرایش شد.")
        return response

    def get_success_url(self)-> str:
        return reverse_lazy("home")


class PostPageView(DetailView):
    model = Post
    template_name = "posts/post_page.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs)-> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["commentform"] = CommentCreateForm()
        return context


class CommentSentViwe:
    pass


class CommentDeleteView:
    pass


