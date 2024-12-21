import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from Post.form import PostCreateForm, PostEditForm
from Post.models import Post, Tag


class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag")
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            return Post.objects.filter(tags__slug=tag_slug)
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Tag.objects.all()
        if hasattr(self, "tag"):
            context["selected_tag"] = self.tag
        return context


class PostCreateView(View):
    template_name = "posts/post_create_view.html"

    def get(self, request, *args, **kwargs):
        form = PostCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                url = form.cleaned_data["url"]
                if not url:
                    raise ValueError("URL cannot be empty.")

                metadata = self.fetch_metadata(url)
                post.image = metadata.get("image")
                post.title = metadata.get("title", "Unknown Title")
                post.artist = metadata.get("artist", "Unknown Artist")

                post.save()
                form.save_m2m()
                return redirect("home")
            except (requests.RequestException, IndexError, ValueError) as e:
                return HttpResponse(
                    f"An error occurred while processing the URL: {e}", status=400
                )
        return render(request, self.template_name, {"form": form})

    @staticmethod
    def fetch_metadata(url):
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


class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("home")
    success_message = "پست با موفقیت حذف شد"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class PostEditView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_page.html"
    context_object_name = "post"
