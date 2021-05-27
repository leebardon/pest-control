# Pest Control

A personal project that I'm undertaking for the sole purpose of properly learning unit and integration testing with Pytest and Django.

Why?

> 1. I'm done with spending countless hours trying to track down the source of a bug;
> 2. I think my code will ultimately be cleaner and more robust with a test-first approach.

## Overview

Basic idea - a webapp that lists universities that are currently hiring for faculty positions, or laying off staff. Based on teaching materials created by Eden Marco for his Udemy course "Real World Python Test Automantion with Pytest".

## Setup Env

Ensure pipenv is installed then run:

```bash
pipenv shell
pipenv install pytest
```

## Setup Django

Next, install Django and set up a basic Django application:

```bash
pipenv install djangorestframework
mkdir api
cd api
django-admin startproject pestcontrol
```

Check if you can launch the Django server, run DB migrations, check admin panel (/admin):

```bash
python manage.py runserver
python manage.py migrate
```

Set yourself up as admin by typing below command and following instructions, run server and log in:

```bash
python manage.py createsuperuser
```

### Create Django Application

We previously created a project (pestcontrol). Django uses the term "Application" for different functional components of a project, so let's create one:

```bash
python manage.py startapp universities
```

### Creating Django Models

The model will create instances of objects that we store in our database. In this case, each object represents a university, and info such as name, when the object was created, website, comments etc. Open models.py within the 'universities' directory and create a class called University that inherits from the Django model class. Give desired attributes.

Example:

```python
class Universities(model.Models):
    name = models.CharField(max_length=50, unique=True)
```

Once the class attributes are defined, add the application to the "installed apps" list in pestcontrol/settings.py. Also add 'rest_framework'. Then create your migrations;

```bash
python manage.py makemigrations universities
```

Migrations are Django's (and web frameworks in general) way to propagate changes you make to your models, into your database. Once the migrations are created, they need to be applied, and the model needs to be registered to Django admin:

```bash
python manage.py migrate
```

Then go to universities/admin.py and add:

```python
from .models import University

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass
```

You can then reload the server, and 'Universities' should be an option in your admin panel. You can add a university using your dfined attributes. Do so, and save. It will display as a "University object" in the list - not super useful.

We need to add a "dunder" (double under) str function to our model and refresh the page, so we can display the object's name, rather then a generic reference:

```python
def __str__(self):
    return self.name
```
