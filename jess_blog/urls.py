"""
Jess_blog URL Configuration
"""

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from post.views import homepage, post, category, about

urlpatterns = [
    path("", homepage, name="homepage"),
    path("ajax/", homepage, name="ajax_homepage"),
    path("post/<str:post_slug>", post, name="post"),
    path("ajax/post/<str:post_slug>", post, name="ajax_post"),
    path("category/<str:category_slug>", category, name="category"),
    path("ajax/category/<str:category_slug>", category, name="ajax_category"),
    path("about", about, name="about"),
    path("ajax/about", about, name="ajax_about"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
