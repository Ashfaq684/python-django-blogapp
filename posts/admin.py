from django.contrib import admin
from .models import Comments, Post, Tag, WebsiteMeta

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(WebsiteMeta)