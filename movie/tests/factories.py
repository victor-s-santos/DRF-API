from datetime import datetime

import factory

from movie.models import Category, Movie
from person.tests.factories import ActorFactory, AuthorFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_name = "CategoryTest"


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = "TestMovie"
    category = factory.SubFactory(Category)
    synopsis = "Test Synopsis"
    publication_date = datetime.now()
    main_actor = factory.SubFactory(ActorFactory)
    main_author = factory.SubFactory(AuthorFactory)
    score = 5.0
