import json

from django.db.models import Count
from django.db.models.aggregates import StdDev

from rest_framework import serializers

from movie.models import Category, Movie
from person.models import Actor, Author


class CategorySerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Category
        fields = ("category_name",)


class MovieSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "category",
            "synopsis",
            "publication_date",
            "main_author",
            "main_actor",
            "score",
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    category = serializers.ReadOnlyField(source="category.category_name")
    main_author = serializers.ReadOnlyField(source="main_author.name")
    main_actor = serializers.ReadOnlyField(source="main_actor.name")
    amount_author_female = serializers.SerializerMethodField()
    amount_author_male = serializers.SerializerMethodField()

    def get_amount_author_female(self, obj):
        """Retorna o número de autores do sexo feminino para este filme"""
        amount_author = Movie.objects.filter(
            id=obj.id, main_author__genre=1
        ).aggregate(Count("main_author"))
        return amount_author

    def get_amount_author_male(self, obj):
        """Retorna o número de autores do sexo masculino para este filme"""
        amount_author = Movie.objects.filter(
            id=obj.id, main_author__genre=2
        ).aggregate(Count("main_author"))
        return amount_author

    class Meta:
        model = Movie
        fields = "__all__"


class MovieStatisticSerializer(serializers.ModelSerializer):
    """Um serializers para trazer dados estatísticos"""

    amount_movies_category = serializers.SerializerMethodField()
    best_movies_category = serializers.SerializerMethodField()
    worst_movies_category = serializers.SerializerMethodField()
    general_standard_deviation = serializers.SerializerMethodField()
    standard_deviation_by_category = serializers.SerializerMethodField()

    def get_standard_deviation_by_category(self, obj):
        """Retorna o desvio padrão de score por categoria"""
        movies = Movie.objects.values("category__category_name").annotate(
            Standard_deviation=StdDev("score")
        )
        for movie in movies:
            if not (movie["Standard_deviation"]):
                movie["Standard_deviation"] = 0
        return movies

    def get_general_standard_deviation(self, obj):
        """Retorna o desvio padrão de score"""
        movies = Movie.objects.all().aggregate(
            Standard_deviation=StdDev("score")
        )
        return movies

    def get_worst_movies_category(self, obj):
        """Retorna a pior nota de cada categoria"""
        movies = (
            Movie.objects.values("category__category_name", "title", "score")
            .order_by("category", "score")
            .distinct("category")
        )
        return movies

    def get_best_movies_category(self, obj):
        """Retorna a melhor nota de cada categoria"""
        movies = (
            Movie.objects.values("category__category_name", "title", "score")
            .order_by("category", "-score")
            .distinct("category")
        )
        return movies

    def get_amount_movies_category(self, obj):
        """Retorna o número de filmes cadastrado de cada categoria"""
        movies = Movie.objects.values("category__category_name").annotate(
            amount=Count("title")
        )
        return movies

    class Meta:
        model = Movie
        fields = (
            "amount_movies_category",
            "best_movies_category",
            "worst_movies_category",
            "general_standard_deviation",
            "standard_deviation_by_category",
        )
