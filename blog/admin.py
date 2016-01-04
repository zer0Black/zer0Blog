from django.contrib import admin

from .models import Post, Catalogue, Carousel, Tag, User, Comment


admin.site.register(Post)
admin.site.register(Catalogue)
admin.site.register(Carousel)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Comment)
