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

    if not os.path.exists(react_types_folder):
        os.makedirs(react_types_folder)

    model_definitions = {}
    model_imports = {}

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

            if f"{app_name}.{model_name}" in default_apps:
                continue

            fields = model._meta.fields + model._meta.many_to_many
            react_fields = []
            imports = set()

            print("Meta fields:", model._meta.fields)
            print("Meta many_to_many:", model._meta.many_to_many)

            print("Full fields:", fields)

            print("Model:", model_name)
            for field in fields:
                print("Field:", field)
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

            imports_code = "\n".join(sorted(imports))
            fields_code = "\n".join(react_fields)
            type_definition = (
                f"{imports_code}\n\n"
                f"export type {model_name} = {{\n{fields_code}\n}};"
            )

            model_definitions[model_name] = type_definition
            model_imports[model_name] = imports_code

    for model_name, type_definition in model_definitions.items():
        output_file = os.path.join(react_types_folder, f"{model_name}.tsx")
        with open(output_file, "w") as f:
            f.write(type_definition)
        print(f"React type for {model_name} saved to {output_file}")


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
