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

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
            "genre",
            "birth_date",
            "nationality",
            "score_average",
        )


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Um serializer simples"""

    genre = serializers.ReadOnlyField(source="get_genre_display")

    class Meta:
        model = Author
        fields = ("name", "genre", "birth_date", "nationality")
