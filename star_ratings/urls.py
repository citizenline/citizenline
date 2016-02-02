from django.conf.urls import patterns, url
from .views import Rate


urlpatterns = patterns(
    '',
    url(r'(?P<slug>\w+)/(?P<question_id>\d+)/', Rate.as_view(), name='rate'),
)
