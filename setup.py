from setuptools import setup, find_packages

setup(
    name="django-react-types",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "generate-react-types = django_react_types.core:generate_and_save_types",
        ],
    },
    author="Diogo Antonio",
    author_email="dabpereiradev@gmail.com",
    description="A Django library to convert models to React types",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bohredd/django-react-types",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
    ],
)
