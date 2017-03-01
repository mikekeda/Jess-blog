from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from post.models import Post


def get_allowed_visibilities(user):
    """Helper function to get allowed visibilities for the user."""

    allowed_visibilities = ['all']
    if user.is_authenticated:
        allowed_visibilities.append('user')
    if user.is_superuser:
        allowed_visibilities.append('admin')

    return allowed_visibilities


def homepage(request):
    """Home page."""

    allowed_visibilities = get_allowed_visibilities(request.user)

    posts = Post.objects.filter(visibility__in=allowed_visibilities).order_by('-id').prefetch_related('categories').prefetch_related('photos')
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts.html', dict(posts=posts, user=request.user, full_text=False, active_page="home"))


def category(request, category_slug):
    """Posts for specific category."""

    allowed_visibilities = get_allowed_visibilities(request.user)

    posts = Post.objects.filter(categories__slug=category_slug, visibility__in=allowed_visibilities).order_by('-id').prefetch_related('categories').prefetch_related('photos')

    return render(request, 'posts.html', dict(posts=posts, user=request.user))


def post(request, post_slug):
    """Post page."""

    post_obj = get_object_or_404(Post.objects.prefetch_related('categories').prefetch_related('photos'), slug=post_slug)
    allowed_visibilities = get_allowed_visibilities(request.user)

    if post_obj.visibility in allowed_visibilities:
        return render(request, 'posts.html', dict(posts=[post_obj], user=request.user, full_text=True))

    return HttpResponseForbidden()


def about(request):
    """About page."""

    return render(request, 'about.html', dict(active_page="about"))
