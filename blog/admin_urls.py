from django.conf.urls import url,include

from blog.admin_views import PostView, DeletePost, NewPost, GetUpdatePost, AddPost, \
    UpdateDraft, UpdatePost, UpdateEditor

urlpatterns = [
    url(r'^admin/', include([
        url(r'^$', PostView.as_view(), name='index'),
        url(r'^delete/(?P<pk>[0-9]+)$', DeletePost.as_view()),
        url(r'^new$', NewPost.as_view()),
        url(r'^add$', AddPost.as_view()),
        url(r'^update/draft/(?P<pk>[0-9]+)$', UpdateDraft.as_view()),
        url(r'^update/post/(?P<pk>[0-9]+)$', UpdatePost.as_view()),
        url(r'^update/(?P<pk>[0-9]+)$', GetUpdatePost.as_view()),
        url(r'^update/editor$', UpdateEditor.as_view()),
    ])),
]