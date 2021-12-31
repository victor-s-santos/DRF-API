from datetime import datetime

import factory

from person.models import Actor, Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = "AuthorTest"
    genre = 1
    birth_date = datetime.now()
    nationality = "PythonLandia"


class ActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actor

    name = "ActorTest"
    genre = 2
    birth_date = datetime.now()
    nationality = "PythonLandia"
