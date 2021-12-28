from django.urls import path

from movie.views import (
    AddActorToMovieView,
    CategoryListCreateView,
    MovieListCreateView,
    MovieRetrieveUpdateDestroyView,
)


urlpatterns = [
    path("", MovieListCreateView.as_view(), name="movies"),
    path(
        "<int:movie_id>/",
        MovieRetrieveUpdateDestroyView.as_view(),
        name="movie_detail",
    ),
    path("category/", CategoryListCreateView.as_view(), name="categories"),
    path(
        "add_actor_to_movie/<int:movie_id>/",
        AddActorToMovieView.as_view(),
        name="add_actor_to_movie",
    ),
]
