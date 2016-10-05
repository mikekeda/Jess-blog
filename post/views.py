from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from post.models import Post


def homepage(request):
    """Main page."""

    posts = Post.objects.order_by('-id').prefetch_related('categories').prefetch_related('photos')
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


def categoty(request, category_slug):
    """Post for specific category."""

    posts = Post.objects.filter(categories__slug=category_slug).order_by('-id').prefetch_related('categories').prefetch_related('photos')

    return render(request, 'posts.html', dict(posts=posts, user=request.user))


def post(request, post_slug):
    """Post for specific category."""

    post = get_object_or_404(Post.objects.prefetch_related('categories').prefetch_related('photos'), slug=post_slug)

    return render(request, 'posts.html', dict(posts=[post], user=request.user, full_text=True))


def about(request):
    """About page."""

    return render(request, 'base.html', dict(active_page="about"))
