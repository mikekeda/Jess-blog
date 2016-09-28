from django.contrib import admin
from django.db import models
from django import forms
from post.models import Category, Post


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})},}

    class Media:
        js = ('bower_components/ckeditor/ckeditor.js',)
        css = {'all': ('css/admin-fix.css',)}

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
