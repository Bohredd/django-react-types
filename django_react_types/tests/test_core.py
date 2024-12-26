import os
import unittest
from django.apps import apps
import django
from django_react_types.core import generate_react_types
from django.core.exceptions import ImproperlyConfigured

class GenerateReactTypesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up any state for the test case."""
        super().setUpClass()

        os.environ["DJANGO_SETTINGS_MODULE"] = (
            "django_react_types.tests.test_settings"  
        )
        django.setup()

    def setUp(self):
        """Runs before each test."""
        self.react_types_folder = "test_react_types"
        self.django_project = "django_react_types"
        self.django_app = "myapp"  

    def tearDown(self):
        """Runs after each test."""
        if os.path.exists(self.react_types_folder):
            for file in os.listdir(self.react_types_folder):
                file_path = os.path.join(self.react_types_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.react_types_folder)

    def test_generate_react_types_for_single_app(self):
        generate_react_types(
            self.django_project, self.react_types_folder, self.django_app
        )

        self.assertTrue(os.path.exists(self.react_types_folder))

        app_models = apps.get_app_config(self.django_app).get_models()
        for model in app_models:
            model_name = model.__name__
            file_path = os.path.join(self.react_types_folder, f"{model_name}.tsx")
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, "r") as f:
                content = f.read()
                self.assertIn(f"export type {model_name}", content)
                self.assertIn("}", content)

    def test_generate_react_types_for_all_apps(self):
        generate_react_types(self.django_project, self.react_types_folder)

        self.assertTrue(os.path.exists(self.react_types_folder))

        for app in apps.get_app_configs():
            for model in app.get_models():
                model_name = model.__name__
                file_path = os.path.join(self.react_types_folder, f"{model_name}.tsx")
                self.assertTrue(os.path.exists(file_path))
                with open(file_path, "r") as f:
                    content = f.read()
                    self.assertIn(f"export type {model_name}", content)
                    self.assertIn("}", content)

    def test_directory_creation(self):
        non_existent_folder = "non_existent_folder"

        if os.path.exists(non_existent_folder):
            os.rmdir(non_existent_folder)

        generate_react_types(self.django_project, non_existent_folder, self.django_app)

        self.assertTrue(os.path.exists(non_existent_folder))

        for file in os.listdir(non_existent_folder):
            os.remove(os.path.join(non_existent_folder, file))
        os.rmdir(non_existent_folder)

    def test_invalid_django_app(self):
        with self.assertRaises(LookupError):
            generate_react_types(
                self.django_project, self.react_types_folder, "invalidapp"
            )