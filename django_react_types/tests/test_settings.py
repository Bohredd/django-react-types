INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "django_react_types", 
    "django_react_types.tests.myapp",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db.sqlite3",
    }
}

SECRET_KEY = "test-secret-key"
