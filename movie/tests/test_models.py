from datetime import date

import pytest

from movie.models import Category, Movie
from person.models import Actor, Author


class Test_models:
    @pytest.mark.django_db
    def test_create_category(self):
        len0 = Category.objects.all().count()
        category_obj = Category.objects.create(category_name="Test category")
        len1 = Category.objects.all().count()
        assert len1 > len0, 1 > 0
        assert Category.objects.get(id=1).category_name == "Test category"

    @pytest.mark.django_db
    def test_create_movie(self, author_obj, actor_obj, category_obj):
        date_now = date.today()
        movie = Movie.objects.create(
            title="Title test",
            category=category_obj,
            synopsis="Synopsis test",
            publication_date=date_now,
        )
        movie.main_actor.add(actor_obj.id)
        movie.main_author.add(author_obj.id)
        assert Movie.objects.all().count() == 1
        assert Movie.objects.get(id=1).title == "Title test"
        assert Movie.objects.get(id=1).category.category_name == "Category Test"
        assert Movie.objects.get(id=1).synopsis == "Synopsis test"
        assert Movie.objects.get(id=1).publication_date == date_now
        assert Movie.objects.get(id=1).main_actor.first().name == "Actor Test"
        assert Movie.objects.get(id=1).main_author.first().name == "Author Test"
