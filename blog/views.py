# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.views.generic import DetailView, ListView

from .models import Post, Carousel


class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    queryset = Post.objects.filter(status=1)  # 只取出状态为“已发布”的文章

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_page_list'] = Carousel.objects.all()
        return context