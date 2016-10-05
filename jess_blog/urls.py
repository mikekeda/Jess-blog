"""jess_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from post.views import homepage, post, categoty, about

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^ajax/$', homepage, name='ajax_homepage'),
    url(r'^post/(?P<post_slug>.+)/$', post, name='post'),
    url(r'^ajax/post/(?P<post_slug>.+)/$', post, name='ajax_post'),
    url(r'^category/(?P<category_slug>.+)/$', categoty, name='category'),
    url(r'^ajax/category/(?P<category_slug>.+)/$', categoty, name='ajax_category'),
    url(r'^about/$', about, name='about'),
    url(r'^ajax/about/$', about, name='ajax_about'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

