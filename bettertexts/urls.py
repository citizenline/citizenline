from django.urls import path

from . import views

app_name = "bettertexts"

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /bettertexts/5/
    path("<slug>/", views.detail, name="detail"),
    # ex: /bettertexts/5/results/
    path("<int:text_id>/results/", views.results, name="results"),
    # ex: /bettertexts/5/vote/
    path("<int:text_id>/vote/", views.vote, name="vote"),
]
