# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.views.generic import View, DetailView, ListView
from django.db.models import Count

from blog.pagination import paginator_tool

from .models import Post, Carousel, Comment


def post(requst):
    return render_to_response('blog/post.html',)


class BaseMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['hot_article_list'] = Post.objects.order_by("view_count")[0:10]
            context['man_list'] = get_user_model().objects.annotate(Count("post"))
        except Exception as e:
            pass

        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    queryset = Post.objects.filter(status=1)  # 只取出状态为“已发布”的文章

    def get_context_data(self, **kwargs):
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.queryset)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_page_list'] = Carousel.objects.all()
        context['page_range'] = page_range
        context['objects'] = objects
        return context


class PostView(BaseMixin, DetailView):
    template_name = 'blog/post.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        pkey = self.kwargs.get("pk")
        context['comment_list'] = self.queryset.get(pk=pkey).comment_set.all()
        return context


class CommentView(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 获取评论
        comment = self.request.POST.get("comment", "")
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        if not comment:
            return HttpResponse(u"请输入评论", status=403)
        if len(comment) > 200:
            return HttpResponse(u"评论过长，请重新输入", status=403)

        # 获取用户IP地址
        if request.META.has_key("HTTP_X_FORWARDED_FOR"):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        pkey = self.kwargs.get("pk", "")
        post_foreignkey = Post.objects.get(pk=pkey)

        comment = Comment.objects.create(
            post=post_foreignkey,
            author=user,
            content=comment,
            ip_address=ip,
        )

        # 返回当前评论
        html = "<li>\
                    <div class=\"blog-comment-content\">\
                        <a><h1>"+comment.author.name+"</h1></a>"\
                        + u"<p>" + comment.content + "</p>"+\
                        "<p>" + comment.publish_Time.strftime("%Y-%m-%d %H:%I:%S")+"</p>\
                    </div>\
                </li>"

        return HttpResponse(html)