from django.db.models import Max

from rest_framework import serializers

from movie.models import Movie
from person.models import Actor, Author


class ActorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Actor
        fields = "__all__"


class ActorDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")
    count_works = serializers.SerializerMethodField()

    def get_count_works(self, obj):
        """Retorna o número de trabalhos que o ator fez"""
        count_works = Movie.objects.filter(main_actor=obj.id).count()
        return count_works

    class Meta:
        model = Actor
        fields = ("name", "genre", "birth_date", "nationality", "count_works")


class AuthorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Author
        fields = "__all__"


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")

    class Meta:
        model = Author
        fields = ("name", "genre", "birth_date", "nationality", "score_average")


class AuthorStatisticSerializer(serializers.ModelSerializer):
    """Um serializer para trazer valores estatísticos"""

    author_best_movie = serializers.SerializerMethodField()
    author_worst_movie = serializers.SerializerMethodField()

    def get_author_worst_movie(self, obj):
        """Retorna o filme de menor score para cada combinação autor categoria"""
        movies = (
            Movie.objects.values(
                "category__category_name", "title", "main_author__name", "score"
            )
            .order_by("category", "main_author__name", "score")
            .distinct("category", "main_author__name")
        )
        return movies

    def get_author_best_movie(self, obj):
        """Retorna o filme de maior score para cada combinação autor categoria"""
        movies = (
            Movie.objects.values(
                "category__category_name", "title", "main_author__name", "score"
            )
            .order_by("category", "main_author__name", "-score")
            .distinct("category", "main_author__name")
        )
        return movies

    class Meta:
        model = Author
        fields = ("author_best_movie", "author_worst_movie")
