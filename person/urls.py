from django.urls import path

from person.views import (
    ActorListCreateView,
    ActorRetrieveUpdateDestroyView,
    AuthorListCreateView,
)


urlpatterns = [
    path("actor/", ActorListCreateView.as_view(), name="actor"),
    path(
        "actor/<int:actor_id>",
        ActorRetrieveUpdateDestroyView.as_view(),
        name="actor_detail",
    ),
    path("author/", AuthorListCreateView.as_view(), name="author"),
]
