from datetime import date, datetime

import pytest

from movie.models import Category, Movie
from person.models import Actor, Author


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def actor_obj():
    actor = Actor.objects.create(
        name="Actor Test",
        genre=1,
        birth_date=datetime.now(),
        nationality="Pythonic",
    )
    actor.save()
    return actor


@pytest.fixture
def actor_obj2():
    actor = Actor.objects.create(
        name="Actor Test2",
        genre=1,
        birth_date=datetime.now(),
        nationality="Pythonic",
    )
    actor.save()
    return actor


@pytest.fixture
def author_obj():
    author = Author.objects.create(
        name="Author Test",
        genre=1,
        birth_date=datetime.now(),
        nationality="Pythonic",
    )
    author.save()
    return author


@pytest.fixture
def author_obj2():
    author = Author.objects.create(
        name="Author Test2",
        genre=1,
        birth_date=datetime.now(),
        nationality="Pythonic",
    )
    author.save()
    return author


@pytest.fixture
def category_obj():
    category = Category.objects.create(category_name="Category Test")
    category.save()
    return category


@pytest.fixture
def movie_obj(category_obj, actor_obj, author_obj):
    movie = Movie.objects.create(
        title="Movie Test",
        category=category_obj,
        synopsis="Synopsis Test",
        publication_date=date.today(),
    )
    movie.main_actor.add(actor_obj.id)
    movie.main_author.add(author_obj.id)
    return movie


@pytest.fixture
def category_obj2():
    category = Category.objects.create(category_name="Category Test 2")
    category.save()
    return category
