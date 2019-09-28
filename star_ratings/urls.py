from django.conf.urls import url
from .views import Rate

app_name = "ratings"

urlpatterns = [url(r"(?P<slug>\w+)/(?P<question_id>\d+)/", Rate.as_view(), name="rate")]
