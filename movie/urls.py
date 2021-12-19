from django.urls import path
from movie.views import MovieListCreateView, CategoryListCreateView


urlpatterns = [
    path('', MovieListCreateView.as_view(), name='movies'),
    path('category/', CategoryListCreateView.as_view(), name='categories'),
]