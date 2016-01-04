from django.conf.urls import url

from blog.views import IndexView, PostView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^post/(?P<pk>[0-9]+)$', PostView.as_view()),
]