"""
Jess_blog URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from post.views import homepage, post, category, about

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^ajax/$', homepage, name='ajax_homepage'),
    url(r'^post/(?P<post_slug>.+)$', post, name='post'),
    url(r'^ajax/post/(?P<post_slug>.+)$', post, name='ajax_post'),
    url(r'^category/(?P<category_slug>.+)$', category, name='category'),
    url(r'^ajax/category/(?P<category_slug>.+)$', category, name='ajax_category'),
    url(r'^about$', about, name='about'),
    url(r'^ajax/about$', about, name='ajax_about'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

