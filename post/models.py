from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    """Taxonomy model"""
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (
            self.name,
        )


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=60, unique=True)
    text = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='category')
    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (
            self.title,
        )
