from person.models import Actor, Author
from rest_framework import serializers


class ActorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""
    class Meta:
        model = Actor
        fields = ("name", "genre", "birth_date", "nationality")


class AuthorSerializer(serializers.ModelSerializer):
    """Um serializer simples"""
    class Meta:
        model = Author
        fields = ("name", "genre", "birth_date", "nationality")