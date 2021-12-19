from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from movie.models import Category, Movie
from movie.serializers import CategorySerializer, MovieSerializer


class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get(self, request):
        movies = Movie.objects.all()
        serializer_class = MovieSerializer(movies, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer_class = CategorySerializer(categories, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
