from django.db import models
from person.models import Author, Actor

class Category(models.Model):
    category_name = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    synopsis = models.TextField(default="Sinópse do filme")
    publication_date = models.DateField()
    main_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    main_author = models.ForeignKey(Author, on_delete=models.CASCADE)
