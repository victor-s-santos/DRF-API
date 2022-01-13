from rest_framework import serializers

from movie.models import Category, Movie


class CategorySerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Category
        fields = (
            "id",
            "category_name",
        )


class MovieSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "category",
            "publication_date",
            "main_author",
            "main_actor",
            "score",
        )


class MovieDetailSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source="category.category_name")
    main_author = serializers.SerializerMethodField("get_main_author")
    main_actor = serializers.SerializerMethodField("get_main_actor")

    def get_main_actor(self, object):
        movie = Movie.objects.get(id=object.id)
        list_actors = []
        for actor in movie.main_actor.all():
            list_actors.append(actor.name)
        return list_actors

    def get_main_author(self, object):
        """The same as above but using list comprehension"""
        movie = Movie.objects.get(id=object.id)
        return [author.name for author in movie.main_author.all()]

    class Meta:
        model = Movie
        fields = ("title", "category", "main_author", "main_actor", "score")


class NestedPersonFilterSerializer(serializers.ModelSerializer):

    author_name = serializers.SerializerMethodField("get_author_name")
    author_genre = serializers.SerializerMethodField("get_author_genre")
    author_score = serializers.SerializerMethodField("get_author_score")

    def get_author_name(self, object):
        movie = Movie.objects.get(id=object.id)
        list_authors = []
        for author in movie.main_author.all():
            list_authors.append(author.name)
        return list_authors

    def get_author_genre(self, object):
        movie = Movie.objects.get(id=object.id)
        list_authors = []
        for author in movie.main_author.all():
            list_authors.append(author.get_genre_display())
        return list_authors

    def get_author_score(self, object):
        movie = Movie.objects.get(id=object.id)
        list_authors = []
        for author in movie.main_author.all():
            list_authors.append(author.score_average)
        return list_authors

    class Meta:
        model = Movie
        fields = ("author_name", "author_genre", "author_score")


class MoviePersonDetailSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source="category.category_name")
    person = serializers.SerializerMethodField("get_person")

    def get_person(self, object):
        movie = Movie.objects.get(id=object.id)
        return NestedPersonFilterSerializer(movie, many=False).data

    class Meta:
        model = Movie
        fields = ("title", "category", "person")
