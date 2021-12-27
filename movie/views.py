from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from movie.models import Category, Movie
from movie.serializers import (
    CategorySerializer,
    MovieDetailSerializer,
    MovieSerializer,
)


class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get(self, request):
        movies = Movie.objects.all()
        serializer_class = MovieSerializer(movies, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer

    def get(self, request, movie_id: int = None):
        movie_detail = Movie.objects.get(id=movie_id)
        serializer_class = MovieDetailSerializer(movie_detail, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def patch(self, request, movie_id: int = None):
        try:
            title = request.data["title"]
            category = request.data["category"]
            synopsis = request.data["synopsis"]
            publication_date = request.data["publication_date"]
            main_actor = request.data["main_actor"]
            main_author = request.data["main_author"]
        except AssertionError as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            movie_detail = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                f"Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = MovieDetailSerializer(
            movie_detail, data=request.data, partial=False
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                serializer_class.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, movie_id: int = None):
        try:
            movie_detail = Movie.objects.get(id=movie_id)
            print(movie_detail)
        except Movie.DoesNotExist:
            return Response(
                f"Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            movie_detail.delete()
            return Response(
                f"Movie has been deleted successfully!",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )


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
