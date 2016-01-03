from django.conf.urls import url

from blog.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
]