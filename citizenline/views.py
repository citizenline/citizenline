from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()

        return context


def robots(request):
    return render(request, "robots.txt", content_type="text/plain")
