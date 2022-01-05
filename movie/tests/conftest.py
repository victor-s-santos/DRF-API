from datetime import datetime

import pytest

from movie.models import Category
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
def category_obj():
    category = Category.objects.create(category_name="Category Test")
    category.save()
    return category
