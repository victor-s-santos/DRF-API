from rest_framework import serializers

from movie.models import Category, Movie


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
            "publication_date",
            "main_author",
            "main_actor",
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    category = serializers.ReadOnlyField(source="category.category_name")
    main_author = serializers.ReadOnlyField(source="main_author.name")
    main_actor = serializers.ReadOnlyField(source="main_actor.name")

    class Meta:
        model = Movie
        fields = "__all__"
