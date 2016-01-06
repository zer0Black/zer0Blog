from django.conf.urls import url

from blog.views import IndexView, PostView, CommentView, RepositoryView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^post/(?P<pk>[0-9]+)$', PostView.as_view()),
    url(r'^comment/(?P<pk>[0-9]+)$', CommentView.as_view()),
    url(r'^repository$', RepositoryView.as_view()),

]