from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from Post.models import Post
from Post.form import PostCreateForm


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
#      form = PostCreateForm()
#      if request.method == 'POST':
#          form = PostCreateForm(request.POST)
#          if form.is_valid():
#              form.save()
#              return redirect('home')
#      return render(request, 'posts/post_create_view.html', {'form': form})


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create_view.html"
    success_url = reverse_lazy("home")
