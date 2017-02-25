from django.contrib import admin
from django.db import models
from django import forms
from post.models import Category, Post, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    min_num = 1
    extra = 0

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})},}
    inlines = (PhotoInline,)

    class Media:
        js = ('bower_components/ckeditor/ckeditor.js',)
        css = {'all': ('css/admin-fix.css',)}

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
