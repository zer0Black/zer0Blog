# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import DetailView, ListView
from django.db.models import Count

from .models import Post, Carousel, User


def post(requst):
    return render_to_response('blog/post.html',)


class BaseMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['hot_article_list'] = Post.objects.order_by("view_count")[0:10]
            context['man_list'] = User.objects.annotate(Count("post"))
        except Exception as e:
            pass

        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    queryset = Post.objects.filter(status=1)[0:10]  # 只取出状态为“已发布”的文章

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_page_list'] = Carousel.objects.all()
        return context


class PostView(BaseMixin, DetailView):
    template_name = 'blog/'