from django.conf.urls import url

from . import views

app_name = 'bettertexts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /bettertexts/5/
    url(r'^(?P<slug>[\w]+)/$', views.detail, name='detail'),
    # ex: /bettertexts/5/results/
    url(r'^(?P<text_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /bettertexts/5/vote/
    url(r'^(?P<text_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
