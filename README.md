# Pest Control

A personal project that I'm undertaking for the sole purpose of properly learning unit and integration testing with Pytest and Django.

Why?

> 1. I'm done with spending countless hours trying to track down the source of a bug;
> 2. I think my code will ultimately be cleaner and more robust with a test-first approach.

## Overview

Basic idea - a webapp that lists universities that are currently hiring for faculty positions, or laying off staff. Based on teaching materials created by Eden Marco for his Udemy course "Real World Python Test Automantion with Pytest".

### Setup Env

Ensure pipenv is installed then run:

```bash
pipenv shell
pipenv install pytest
```

## Django

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

We need to add a "dunder" (double under) str function to our model and refresh the page, so we can display the object's name, rather then a generic reference. We can also include a type hint (->str) to make the code more readable.

```python
def __str__(self)->str:
    return f"{self.name}"
```

## Creating the Rest API

### Views

Within the universities model folder, create a new file called 'serializers.py'. This will take the model from the database and serialise it into JSON format.

Import the model, and also import the serializers module from rest_framework. Create a class and a Meta subclass telling Django which fields you want to serialize, so they can be displayed on the front end:

```python
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("id", "name", "status", "application_link", "last_update", "notes")
```

### Viewsets

Within the universities model folder, open the views.py file and import ModelViewSet from rest_frameworks.viewsets. Create a class called UniversityViewSet, and have it inherit the Django ModelViewSets class. This basically implements a rest framework on our behalf (check out the class definition to see what it does specifically).

We need to tell the class what we want to serialise, and also the queryset (i.e. what we want to return/view). We also want to specify pagination, so instead of getting a long list of a squillion objects that causes the server to time out, we can break the return into chunks, or return/render only a certain number, etc.

```python
class UniversityViewSet(ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
```

The "objects.all()" syntax is Django's Object Relational Mapper syntax - an object oriented abstraction of the database, to communicate easily without having to write sql queries.

### Configuring URL Routes (Controllers)

Django makes this easy - when we created our ViewSets, it automatically created all the REST functions we need (GET, POST, DELETE, UPDATE, etc). We just need to tell it what endpoints we want to use.

Create a file called urls.py. Here, we instantiate and register a Django DefaultRouter() class, and register it with a prefix, viewset, and basename.

## Testing

- Start with the empty case where we have no universities.
- Test name should begin with what we are testing (test case "zero universites")
- And should end with what we are asserting (returns empty list)
- (Note that test cases will all return None, as we are just asserting, needs no return)
- In this case, as it's a webapp, we use a client to test the calls and responses to and from our endpoints
- import relevant client from Django
- Create a test class and have it inherit the TestCase class from unittest

```python
from unittest import TestCase
from django.test import Client
from django

class TestGetUniversities(TestCase):
    def test_zero_universities_should_return_empty_list(self)->None:
        client = Client()
        response = client.get(universities_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])
```

## PATHS!

This can be extremely frustrating, especially in VSCode, and can cause a lot of issues with modules not being found. First, check current PYTHONPATH:

```bash
echo $PYTHONPATH
```

It might be empty. Add your base directory for the project overall, as well as the path to the specific module. For me, it looks like this:

```bash
export /Users/leebardon/Dropbox/Development/misc/learning-pytest/:/Users/leebardon/Dropbox/Development/misc/learning-pytest/api/pestcontrol/
```

We also need to install Django's test database (pipenv install pytest-django) for the tests to run in this environment. Every time we run the tests, pytest-django will create a "TEST DATABASE" according to our project's schema (i.e. from the migrations).

WHY?

1. NEVER MIX PRODUCTION DB WITH TEST DB
