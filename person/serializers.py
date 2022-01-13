from rest_framework import serializers

from person.models import Actor, Author


class ActorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    class Meta:
        model = Actor
        fields = "__all__"


class ActorDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")

    class Meta:
        model = Actor
        fields = ("name", "genre", "birth_date", "nationality")


class AuthorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")
    movies = serializers.SerializerMethodField(source="get_movies")

    def get_movies(self, obj):
        author = obj
        movies = author.movie_set
        movie_list = []
        for movie in movies.all():
            movie_list.append(movie.title)
        return movie_list
        # return [movie.title for movie in author.movie_set.all()]

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
            "genre",
            "birth_date",
            "nationality",
            "score_average",
            "movies",
        )


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")

    class Meta:
        model = Author
        fields = ("name", "genre", "birth_date", "nationality")
