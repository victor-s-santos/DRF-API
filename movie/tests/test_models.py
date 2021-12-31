import pytest

from movie.models import Category, Movie
from movie.tests.factories import CategoryFactory, MovieFactory
from person.tests.factories import ActorFactory, AuthorFactory


class Test_models:
    @pytest.mark.django_db
    def test_create_category(self):
        len0 = Category.objects.all().count()
        category_obj = Category.objects.create(category_name="Test category")
        len1 = Category.objects.all().count()
        assert len1 > len0, 1 > 0
        assert Category.objects.get(id=1).category_name == "Test category"

    @pytest.mark.django_db
    def test_create_movie(self):
        movie = MovieFactory
        category = CategoryFactory()
        actor = ActorFactory
        autor = AuthorFactory
        len0 = Movie.objects.all().count()
        movie_obj = Movie.objects.create(
            title=movie.title,
            category=category,
            synopsis=movie.synopsis,
            publication_date=movie.publication_date,
            main_actor=actor.name,
            main_author=autor.name,
            score=movie.score,
        )
        len1 = Movie.objects.all().count()
        assert len1 > len0
        assert movie_obj.title == "TestMovie"

    def test_factory_category_use(self):
        category = CategoryFactory
        assert category.category_name == "CategoryTest"

    def test_factory_movie_use(self):
        movie = MovieFactory
        autor = movie.main_author.get_factory().name
        assert autor == "AuthorTest"
