from django.shortcuts import render
from django.views.generic import TemplateView


# TODO : function with test written There is no readability in the code at all
# def home_view(request, **kwargs):
#     return render(request, 'posts/home.html')
class HomeView(TemplateView):
    template_name = "posts/home.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["greeting"] = "سلام، به وب سایت ما خوش آمدید!"
    #     return context
