# Django React Types

A Python package that generates TypeScript types for Django models, making it easier to integrate Django backend models with React frontend applications. This library automatically converts Django models into TypeScript interfaces for easier type checking and better developer experience in your React applications.

## Features

- Automatically generates TypeScript types for all models in your Django project or specific apps.
- Saves generated `.tsx` type files for each model in a specified directory.
- Supports Django apps and projects, allowing you to generate types for a specific app or all apps in the project.
- Easy to install and integrate into your Django project.

## Installation

You can install the `django-react-types` package directly from GitHub:

```bash
pip install git+https://github.com/Bohredd/django-react-types.git
```

### Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/Bohredd/django-react-types.git
cd django-react-types
pip install .
```

##Usage
To generate TypeScript types for your Django models, you can use the provided function generate_react_types. The following parameters are required:

django_project: The name of your Django project.
react_types_folder: The directory where the generated .tsx files will be saved.
django_app (optional): If provided, only the models of this app will be used.

```python
from django_react_types.core import generate_react_types

# Generate TypeScript types for all apps in the Django project
generate_react_types(
    django_project="your_django_project", 
    react_types_folder="path/to/output/folder"
)

# Generate TypeScript types for a specific app
generate_react_types(
    django_project="your_django_project", 
    react_types_folder="path/to/output/folder", 
    django_app="your_app"
)
```

You can use like this too:
```python
generate-react-types --django_project backend.settings --react_types_folder frontend/src/types
```

backend.settings = my project django settings file
frontend/src/types = where the objects types tsx will be saved 

## Options
#### --react_types_folder: The folder where the .tsx files will be generated.
#### --django_app: The specific Django app to generate types for. If omitted, types will be generated for all apps.
####  --django_project: The path to your Django project.


### Example Command Line Usage

```bash
python manage.py generate_react_types --django_project your_django_project --react_types_folder path/to/output/folder --django_app your_app
```

## This project comes with unit tests to ensure everything works as expected. You can run the tests using the following command:

```bash
python manage.py test
```

## Contributing
We welcome contributions to improve the project. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests for the changes you make.
4.Submit a pull request with a detailed explanation of your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Django: A powerful Python web framework used as the backend of this project.
TypeScript: A superset of JavaScript that enables optional static typing.
Contact
For any questions or issues, feel free to open an issue on the repository or contact the project maintainers.
