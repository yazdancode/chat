import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView

from Post.form import PostCreateForm, PostEditForm
from Post.models import Post


# TODO : function with test written There is no readability in the code at all
# def home_view(request, **kwargs):
#     posts = Post.objects.all()
#
#     return render(request, 'posts/home.html', {'posts': posts})
class HomeView(ListView):
    template_name = "posts/home.html"
    model = Post
    context_object_name = "posts"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["greeting"] = "سلام، به وب سایت ما خوش آمدید!"
    #     return context


# TODO: function with test written There is a readability in the code at all
# def post_create_view(request, **kwargs):
#     form = PostCreateForm()
#     if request.method == "POST":
#         form = PostCreateForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             website = request.get(form.data["url"])
#             sourcecode = BeautifulSoup(website.text, "html.parser")
#             find_image = sourcecode.select(
#                 'meta[content^="https://live.staticflickr.com/"]'
#             )
#             image = find_image[0]["content"]
#             post.image = image
#             find_title = sourcecode.select("h1.photo-title")
#             title = find_title[0].text.strip()
#             post.title = title
#             find_artist = sourcecode.select("a.owner-name")
#             artist = find_artist[0].text.strip()
#             post.artist = artist
#             post.save()
#             return redirect("home")
#     return render(request, "posts/post_create_view.html", {"form": form})


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
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                source_code = BeautifulSoup(response.text, "html.parser")
                image_meta = source_code.select(
                    'meta[content^="https://live.staticflickr.com/"]'
                )
                post.image = image_meta[0]["content"] if image_meta else None
                title_element = source_code.select("h1.photo-title")
                post.title = (
                    title_element[0].text.strip() if title_element else "Unknown Title"
                )
                artist_element = source_code.select("a.owner-name")
                post.artist = (
                    artist_element[0].text.strip()
                    if artist_element
                    else "Unknown Artist"
                )
                post.save()
                return redirect("home")

            except (requests.RequestException, IndexError) as e:
                return HttpResponse(
                    f"An error occurred while processing the URL: {e}", status=400
                )
        return render(request, self.template_name, {"form": form})


# TODO: function with test written There is a readability in the code at all
# def post_delete_view(request, pk):
# post = get_object_or_404(Post, id=pk)
#
#     if request.method == "POST":
#         post.delete()
#         messages.success(request, "پست با موفقیت حذف شد")
#         return redirect("home")
#     return render(request, "posts/post_delete.html", {"post": post})


class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("home")
    success_message = "پست با موفقیت حذف شد"

    def delete(self, request, *args, **kwargs):
        # Custom delete logic or additional processing (if needed)
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# TODO: function with test written There is a readability in the code at all
# def post_edit_view(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     form = PostEditForm(instance=post)
#     context = {
#         'post': post,
#         'form': form
#     }
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Post updated')
#             return redirect('home')
#     return render(request, 'posts/post_edit.html', context=context)


class PostUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("home")
    success_message = "پست به روز شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        return context


# TODO: function with test written There is a readability in the code at all
def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, "posts/post_page.html", {"post": post})


# class PostView(View):
#     template_name = "posts/post_page.html"
#     def get(self, request, pk):
#         post = Post.objects.get(id=pk)
#         return render(request, self.template_name, {"post": post})
