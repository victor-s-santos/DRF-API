from django.db import models

class Author(models.Model):
    GENRE_CHOICES = (
        (1, "Female"), (2, "Male")
        )
    name = models.CharField(max_length=200)
    genre = models.IntegerField(choices=GENRE_CHOICES, default=1)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=200)

    
class Actor(models.Model):
    GENRE_CHOICES = (
        (1, "Female"), (2, "Male")
        )
    name = models.CharField(max_length=200)
    genre = models.IntegerField(choices=GENRE_CHOICES, default=1)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=200)
