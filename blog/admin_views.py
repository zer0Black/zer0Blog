# -*- coding:utf-8 -*-
import datetime
import time
import os
import uuid
from django.views.generic import View, ListView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from zer0Blog.settings import MEDIA_ROOT, MEDIA_URL

from zer0Blog.settings import PERNUM
from blog.pagination import paginator_tool
from .models import Post, Catalogue, Editor, Carousel


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
        return context


class UpdatePostIndexView(UpdateView):
    template_name = 'admin/post_new.html'
    model = Post
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(UpdatePostIndexView, self).get_context_data(**kwargs)
        context['catalogue_list'] = Catalogue.objects.all()
        return context


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
        editor_choice_foreignkey = user.editor_choice

        post_obj = Post.objects.create(
            title=title,
            author=user,
            content=content,
            catalogue=catalogue_foreignkey,
            status=action,
            editor_choice=editor_choice_foreignkey,
        )

        post_obj.update_tags(tags)

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
        post.modify_time = datetime.datetime.now()
        post.save()

        post.update_tags(tags)

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
        post.modify_time = datetime.datetime.now()
        post.save()

        post.update_tags(tags)

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


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        from django.contrib.auth.views import logout
        return logout(request, next_page='/')


class CarouselIndexView(ListView):
    template_name = 'admin/carousel_admin.html'
    context_object_name = 'carousel_list'
    queryset = Carousel.objects.all()


class CarouselEditView(CreateView):
    template_name = 'admin/carousel_new.html'
    model = Carousel
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(CarouselEditView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context


class AddCarousel(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        title = request.POST.get("title", "")
        post = request.POST.get("post", "")
        post_foreignkey = Post.objects.get(pk=post)
        image_link = request.POST.get("image_link", "")

        if not image_link:
            filename = ""
            try:
                file_img = request.FILES['files']
                file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name))-1]
                filename = uuid.uuid1().__str__() + file_suffix

                path = MEDIA_ROOT + "/carousel/"
                if not os.path.exists(path):
                    os.makedirs(path)

                file_name = path + filename
                destination = open(file_name, "wb+")
                for chunk in file_img.chunks():
                    destination.write(chunk)
                destination.close()
            except Exception, e:
                print e
            file_img_url = MEDIA_URL + "carousel/" + filename
            Carousel.objects.create(
                title=title,
                post=post_foreignkey,
                img=file_img_url,
            )
        else:
            Carousel.objects.create(
                title=title,
                post=post_foreignkey,
                img=image_link,
            )
        return HttpResponseRedirect('/admin/carousel')


class DeleteCarousel(View):
    def get(self, request, *args, **kwargs):
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        carousel = Carousel.objects.get(id=pkey)
        carousel.delete()
        return HttpResponseRedirect('/admin/carousel')


class CarouselUpdateView(UpdateView):
    template_name = 'admin/carousel_update.html'
    model = Carousel
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(CarouselUpdateView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context


class updateCarousel(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        title = request.POST.get("title", "")
        post = request.POST.get("post", "")
        post_foreignkey = Post.objects.get(pk=post)
        image_link = request.POST.get("image_link", "")

        pkey = self.kwargs.get('pk')
        carousel = Carousel.objects.get(id=pkey)

        if not image_link:
            try:
                file_img = request.FILES['files']
                file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name))-1]
                filename = uuid.uuid1().__str__() + file_suffix

                path = MEDIA_ROOT + "/carousel/"
                if not os.path.exists(path):
                    os.makedirs(path)

                file_name = path + filename
                destination = open(file_name, "wb+")
                for chunk in file_img.chunks():
                    destination.write(chunk)
                destination.close()
            except Exception, e:
                print e
            file_img_url = MEDIA_URL + "carousel/" + filename

            carousel.title = title
            carousel.post = post_foreignkey
            carousel.img = file_img_url
            carousel.save()

        else:
            carousel.title = title
            carousel.post = post_foreignkey
            carousel.img = image_link
            carousel.save()
        return HttpResponseRedirect('/admin/carousel')