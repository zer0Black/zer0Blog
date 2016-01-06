from django.contrib import admin

from .models import Post, Catalogue, Carousel, Tag, Comment, Repository


admin.site.register(Post)
admin.site.register(Carousel)
admin.site.register(Repository)
