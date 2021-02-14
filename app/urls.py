from django.conf.urls import url
from django.views.generic import TemplateView

from app.api.m3u8 import m3u8download

app_name = 'app'
urlpatterns = [
    url(r'^api/m3u8download/',m3u8download.M3u8downloadAPIView.as_view()),
    url(r'^api/index',TemplateView.as_view(template_name='index.html')),
    url(r'^api/video',TemplateView.as_view(template_name='video.html')),
]