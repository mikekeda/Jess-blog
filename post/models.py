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

    def __str__(self):
        return u'%s' % (
            self.name,
        )


class Post(models.Model):
    """Post model"""
    VISIBILITIES = (
        ('nobody', 'Hidden for all'),
        ('admin', 'Visible only for admin'),
        ('user', 'Visible only for resisted user'),
        ('all', 'Visible for all'),
    )

    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=6, choices=VISIBILITIES, default='nobody')
    categories = models.ManyToManyField(Category, related_name='category')
    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, editable=False)

    def _get_unique_slug(self):
        unique_slug = slug = slugify(self.title)
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self._get_unique_slug()

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s' % (
            self.title,
        )


class Photo(models.Model):
    """Photo model"""
    title = models.CharField(blank=True, max_length=60)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos')
    post = models.ForeignKey(Post, related_name='photos')
    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)
