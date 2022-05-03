from django.db.models import Count

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
