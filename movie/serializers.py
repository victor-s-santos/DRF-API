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
        fields = ("category", "main_author", "main_actor", "score")
