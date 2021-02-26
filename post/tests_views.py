from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from post.models import Post
from post.views import get_allowed_visibilities

User = get_user_model()


class JessBlogViewTest(TestCase):
    def setUp(self):
        # Create usual user.
        self.password = User.objects.make_random_password()
        test_user = User.objects.create_user(
            username="testuser", password=self.password
        )
        test_user.save()

        # Create admin user.
        test_admin = User.objects.create_superuser(
            username="testadmin", email="myemail@test.com", password=self.password
        )
        test_admin.save()

        test_post_anonymous = Post(title="test_post_anonymous", visibility="all")
        test_post_anonymous.save()
        test_post_authenticated = Post(
            title="test_post_authenticated", visibility="user"
        )
        test_post_authenticated.save()
        test_post_admin = Post(title="test_post_admin", visibility="admin")
        test_post_admin.save()

    # Helpers functions.
    def test_views_get_allowed_visibilities(self):
        # Anonymous user.
        test_user = AnonymousUser()
        result = get_allowed_visibilities(test_user)
        self.assertEqual(set(result), {"all"})

        # Authenticated user.
        test_user = User.objects.get(username="testuser")
        result = get_allowed_visibilities(test_user)
        self.assertEqual(set(result), {"all", "user"})

        # Admin user.
        test_user = User.objects.get(username="testadmin")
        result = get_allowed_visibilities(test_user)
        self.assertEqual(set(result), {"all", "user", "admin"})

    # Pages available for anonymous.
    def test_views_home(self):
        resp = self.client.get(reverse("homepage"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")

        resp = self.client.get(reverse("homepage") + "/?page=sdf")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")

        resp = self.client.get(reverse("homepage") + "/?page=100")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")

    def test_views_post(self):
        resp = self.client.get(reverse("post", kwargs={"post_slug": "notexists"}))
        self.assertEqual(resp.status_code, 404)

        # Post visible only for all users.
        test_post_anonymous = Post.objects.get(title="test_post_anonymous")
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_anonymous.slug})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")

        # Post visible only for authenticated users.
        test_post_authenticated = Post.objects.get(title="test_post_authenticated")
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_authenticated.slug})
        )
        self.assertEqual(resp.status_code, 403)
        self.client.login(username="testuser", password=self.password)
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_authenticated.slug})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")
        self.client.logout()

        # Post visible only for admins.
        test_post_admin = Post.objects.get(title="test_post_admin")
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_admin.slug})
        )
        self.assertEqual(resp.status_code, 403)
        self.client.login(username="testuser", password=self.password)
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_admin.slug})
        )
        self.assertEqual(resp.status_code, 403)
        self.client.login(username="testadmin", password=self.password)
        resp = self.client.get(
            reverse("post", kwargs={"post_slug": test_post_admin.slug})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "posts.html")

    def test_views_about(self):
        resp = self.client.get(reverse("about"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "about.html")
