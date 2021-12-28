from datetime import date

import pytest

from person.models import Actor, Author


class Test_models:
    @pytest.mark.django_db
    def test_create_author(self):
        len0 = Author.objects.all().count()
        author_obj = Author.objects.create(
            name="Test Author",
            genre=1,
            birth_date=date.today(),
            nationality="Pythonic",
        )
        len1 = Author.objects.all().count()
        assert len1 > len0, 1 > 0
        assert Author.objects.get(id=1).name == "Test Author"

    @pytest.mark.django_db
    def test_create_actor(self):
        len0 = Actor.objects.all().count()
        author_obj = Actor.objects.create(
            name="Test Actor",
            genre=1,
            birth_date=date.today(),
            nationality="Pythonic",
        )
        len1 = Actor.objects.all().count()
        assert len1 > len0, 1 > 0
        assert Actor.objects.get(id=1).name == "Test Actor"
