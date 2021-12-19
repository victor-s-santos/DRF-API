from django.urls import path
from person.views import ActorListCreateView, AuthorListCreateView


urlpatterns = [
    path('actor/', ActorListCreateView.as_view(), name='actor'),
    path('author/', AuthorListCreateView.as_view(), name='author'),
]