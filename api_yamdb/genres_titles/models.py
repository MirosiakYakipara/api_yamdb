from django.db import models

from api.models import Title, Genre


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.genre} {self.title}'

    class Meta:
        app_label ='genres_titles'
    