from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# TODO : function with test written There is no readability in the code at all
def profile_view(request):
    return render(request, "users/profile.html")


class ProfileView(TemplateView):
    template_name = "users/profile.html"
