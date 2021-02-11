from django.conf.urls import url
from django.urls import include
from app.api.m3u8 import m3u8download

app_name = 'app'
urlpatterns = [
    url(r'^api/m3u8download/',m3u8download.M3u8downloadAPIView.as_view()),
]