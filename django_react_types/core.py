import os
import django
import argparse
from django.apps import apps
from django_react_types.types import FIELD_TYPE_MAPPING
from django.core.exceptions import ImproperlyConfigured
from django.db import models


def generate_react_types(
    django_project: str, react_types_folder: str, django_app: str = None
):
    os.environ["DJANGO_SETTINGS_MODULE"] = django_project

    settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
    if not settings_module:
        raise ImproperlyConfigured("The Django settings module is not set.")

    try:
        __import__(settings_module)
        django.setup()
    except ModuleNotFoundError:
        raise ImproperlyConfigured(
            f"The Django settings module '{settings_module}' could not be found."
        )
    except Exception as e:
        raise ImproperlyConfigured(f"Could not configure the Django project: {str(e)}")

    if django_app:
        apps_to_search = [apps.get_app_config(django_app)]
    else:
        apps_to_search = apps.get_app_configs()

    react_types = []

    default_apps = [
        "admin.LogEntry",
        "auth.Permission",
        "auth.Group",
        "auth.User",
        "contenttypes.ContentType",
        "sessions.Session",
        "authtoken.Token",
        "authtoken.TokenProxy",
        "django_celery_beat.SolarSchedule",
        "django_celery_beat.IntervalSchedule",
        "django_celery_beat.ClockedSchedule",
        "django_celery_beat.CrontabSchedule",
        "django_celery_beat.PeriodicTasks",
        "django_celery_beat.PeriodicTask",
        "django_celery_results.TaskResult",
        "django_celery_results.ChordCounter",
        "django_celery_results.GroupResult",
    ]

    for app in apps_to_search:
        for model in app.get_models():

            app_name = model._meta.app_label
            model_name = model.__name__

            if f"{app_name}.{model_name}" not in default_apps:
                fields = model._meta.fields
                react_fields = []
                imports = set()

                for field in fields:
                    if isinstance(field, models.ForeignKey):
                        related_model_name = field.related_model.__name__
                        react_field_type = related_model_name
                        imports.add(
                            f"import {{ {related_model_name} }} from './{related_model_name}';"
                        )
                    elif isinstance(field, models.ManyToManyField):
                        related_model_name = field.related_model.__name__
                        react_field_type = f"{related_model_name}[]"
                        imports.add(
                            f"import {{ {related_model_name} }} from './{related_model_name}';"
                        )
                    else:
                        react_field_type = FIELD_TYPE_MAPPING.get(type(field), "any")

                    react_fields.append(f"{field.name}: {react_field_type};")

                react_type = (
                    f"{'\n'.join(imports)}\n\n"
                    f"export type {model_name} ={{\n" + "\n".join(react_fields) + "\n}"
                )
                react_types.append(react_type)

    if not os.path.exists(react_types_folder):
        os.makedirs(react_types_folder)

    for react_type in react_types:
        model_name = react_type.split()[2]
        output_file = os.path.join(react_types_folder, f"{model_name}.tsx")

        with open(output_file, "w") as f:
            f.write(react_type)
        print(f"React types have been saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate React types from Django models."
    )
    parser.add_argument(
        "--react_types_folder",
        required=True,
        help="The folder where the generated .tsx files will be saved.",
    )
    parser.add_argument(
        "--django_app", help="The specific Django app to search for models (optional)."
    )
    parser.add_argument(
        "--django_project", required=True, help="The path to the Django project."
    )

    args = parser.parse_args()
    generate_react_types(args.django_project, args.react_types_folder, args.django_app)
