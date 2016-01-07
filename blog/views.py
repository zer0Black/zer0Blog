# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.views.generic import View, DetailView, ListView
from django.db.models import Count
from zer0Blog.settings import PERNUM

from blog.pagination import paginator_tool

from .models import Post, Carousel, Comment, Repository


def index(requst):
    return render_to_response('admin/blog_admin.html',)


class BaseMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['hot_article_list'] = Post.objects.order_by("-view_count")[0:10]
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
        objects, page_range = paginator_tool(pages=page, queryset=self.queryset, display_amount=PERNUM)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel_page_list'] = Carousel.objects.all()
        context['page_range'] = page_range
        context['objects'] = objects
        return context


class PostView(BaseMixin, DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status=1)

    # 用于记录文章的阅读量，每次请求添加一次阅读量
    def get(self, request, *args, **kwargs):
        pkey = self.kwargs.get("pk")
        posts = self.queryset.get(pk=pkey)
        posts.view_count += 1
        posts.save()
        return super(PostView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        pkey = self.kwargs.get("pk")
        context['comment_list'] = self.queryset.get(pk=pkey).comment_set.all().order_by('-publish_Time')
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
                        <a><h4>"+comment.author.username+"</h4></a>"\
                        + u"<p>" + comment.content + "</p>"+\
                        "<p>" + comment.publish_Time.strftime("%Y年%m月%d日 %R")+"</p>\
                    </div>\
                </li>"

        return HttpResponse(html)


class RepositoryView(BaseMixin, ListView):
    template_name = 'blog/repository.html'
    context_object_name = 'repository_list'
    queryset = Repository.objects.all()

    def get_context_data(self, **kwargs):
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.queryset, display_amount=PERNUM)
        context = super(RepositoryView, self).get_context_data(**kwargs)
        context['page_range'] = page_range
        context['objects'] = objects
        return context


class RepositoryDetailView(BaseMixin, DetailView):
    template_name = 'blog/repository_detail.html'
    context_object_name = 'repository'
    queryset = Repository.objects.all()

    # 用于记录文章的阅读量，每次请求添加一次阅读量
    def get(self, request, *args, **kwargs):
        pkey = self.kwargs.get("pk")
        repositorys = self.queryset.get(pk=pkey)
        repositorys.view_count += 1
        repositorys.save()
        return super(RepositoryDetailView, self).get(request, *args, **kwargs)
