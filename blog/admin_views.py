# -*- coding:utf-8 -*-
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
import json

from zer0Blog.settings import PERNUM
from blog.pagination import paginator_tool
from .models import Post, Catalogue, Tag, Editor


class PostView(ListView):
    template_name = 'admin/blog_admin.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        user = self.request.user
        post_list = Post.objects.filter(author_id=user.id).exclude(status=2)
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.object_list, display_amount=PERNUM)
        context['page_range'] = page_range
        context['objects'] = objects
        context['editor_list'] = Editor.objects.all()
        return context


class DeletePost(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        post.status = 2
        post.save()
        return HttpResponseRedirect('/admin/')


class NewPost(CreateView):
    template_name = 'admin/post_new.html'
    model = Post
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(NewPost, self).get_context_data(**kwargs)
        context['catalogue_list'] = Catalogue.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context


class GetUpdatePost(UpdateView):
    template_name = 'admin/post_new.html'
    model = Post
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(GetUpdatePost, self).get_context_data(**kwargs)
        context['catalogue_list'] = Catalogue.objects.all()
        context['tag_html'] = self.handle_tag()
        return context

    def handle_tag(self):
        post = self.model.objects.get(pk=self.kwargs.get("pk"))
        html = ""
        for tag in Tag.objects.all():
            if post.tag.all():
                flag = 0
                for exist_tag in post.tag.all():
                    if tag.name == exist_tag.name:
                        flag = 1

                if flag == 1:
                    html += "<option selected value='" + tag.name + "'>" + tag.name + "</option>"
                elif flag == 0:
                    html += "<option value='" + tag.name + "'>" + tag.name + "</option>"

        return html


class AddPost(View):
    def post(self, request):
        # 获取当前用户
        user = request.user
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)

        post_obj = Post.objects.create(
            title=title,
            author=user,
            content=content,
            catalogue=catalogue_foreignkey,
            status=action,
        )

        # 插入多对多关系的标签
        for tag in tags:
            tag_foreignkey = Tag.objects.get(name=tag)
            post_obj.tag.add(tag_foreignkey)

        return HttpResponseRedirect('/admin/')


class UpdateDraft(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user
        # 获取要修改的博客
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)

        post.title = title
        post.content = content
        post.catalogue = catalogue_foreignkey
        post.status = action

        # 删除之前的标签，插入新的
        for tag in post.tag.all():
            post.tag.remove(tag)

        for tag in tags:
            tag_foreignkey = Tag.objects.get(name=tag)
            post.tag.add(tag_foreignkey)

        post.save()

        return HttpResponseRedirect('/admin/')


class UpdatePost(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user
        # 获取要修改的博客
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = 1

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)

        post.title = title
        post.content = content
        post.catalogue = catalogue_foreignkey
        post.status = action

        # 删除之前的标签，插入新的
        for tag in post.tag.all():
            post.tag.remove(tag)

        for tag in tags:
            tag_foreignkey = Tag.objects.get(name=tag)
            post.tag.add(tag_foreignkey)

        post.save()

        return HttpResponseRedirect('/admin/')


class UpdateEditor(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user

        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取编辑器
        editor = request.POST.get("editor", "")
        editor_foreignkey = Editor.objects.get(name=editor)
        user.editor_choice = editor_foreignkey
        user.save()

        return HttpResponseRedirect('/admin/')
