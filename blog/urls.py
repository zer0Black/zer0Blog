from django.conf.urls import url

from blog.views import IndexView, PostView, CommentView, RepositoryView, RepositoryDetailView, TagListView, \
    CategoryListView, AuthorPostListView, CommentDeleteView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^post/(?P<pk>[0-9]+)$', PostView.as_view()),
    url(r'^comment/add/(?P<pk>[0-9]+)$', CommentView.as_view()),
    url(r'^comment/delete/(?P<pk>[0-9]+)$', CommentDeleteView.as_view()),
    url(r'^repository$', RepositoryView.as_view()),
    url(r'^repository/(?P<pk>[0-9]+)$', RepositoryDetailView.as_view()),
    url(r'^tag/(?P<slug>[\w\u4e00-\u9fa5]+)$', TagListView.as_view()),
    url(r'^category/(?P<slug>[\w\u4e00-\u9fa5]+)$', CategoryListView.as_view()),
    url(r'^author/(?P<pk>[0-9]+)$', AuthorPostListView.as_view())
]