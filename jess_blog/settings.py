"""
Django settings for jess_blog project.
"""

import os
import requests

SITE_ENV_PREFIX = "JESS"


def get_env_var(name: str, default: str = "") -> str:
    """Get all sensitive data from google vm custom metadata."""
    try:
        name = f"{SITE_ENV_PREFIX}_{name}"
        res = os.environ.get(name)
        if res:
            # Check env variable (Jenkins build).
            return res
        else:
            res = requests.get(
                "http://metadata.google.internal/computeMetadata/"
                "v1/instance/attributes/{}".format(name),
                headers={"Metadata-Flavor": "Google"},
            )
            if res.status_code == 200:
                return res.text
    except requests.exceptions.ConnectionError:
        return default
    return default


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var(
    "SECRET_KEY", "zha7wy3q_pnfi=)h0zzi!wukd6c^x(s1z*mb-+7j)rby)q_&t7"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(get_env_var("DEBUG", "True"))

INTERNAL_IPS = ("127.0.0.1",)

ALLOWED_HOSTS = get_env_var("ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "post",
]

if DEBUG:
    INSTALLED_APPS += ["django_jenkins", "debug_toolbar"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "jess_blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "post.context_processors.select_parent_template",
            ],
        },
    },
]

WSGI_APPLICATION = "jess_blog.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_var("DB_NAME", "jess_blog"),
        "USER": get_env_var("DB_USER", "jess_blog_admin"),
        "PASSWORD": get_env_var("DB_PASSWORD", "jess_blog_pass_!_64"),
        "HOST": get_env_var("DB_HOST", "127.0.0.1"),
        "PORT": "",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (("", os.path.join(BASE_DIR, "static")),)

STATIC_ROOT = "/home/voron/sites/cdn/jess_blog"

STATIC_URL = "https://storage.googleapis.com/cdn.mkeda.me/jess_blog/"
if DEBUG:
    STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

JENKINS_TASKS = (
    "django_jenkins.tasks.run_pylint",
    "django_jenkins.tasks.run_pep8",
    "django_jenkins.tasks.run_pyflakes",
)

PROJECT_APPS = ["post", "jess_blog"]

PYLINT_LOAD_PLUGIN = ["pylint_django"]
