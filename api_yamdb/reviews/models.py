from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api.models import Title


User = get_user_model()


class Review(models.Model):

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="reviews"
                               )
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    score = models.IntegerField(blank=True,
                                verbose_name='score',
                                validators=[
                                    MinValueValidator(1, 'From 1 to 10'),
                                    MaxValueValidator(10, 'From 1 to 10')
                                ]
                                )
    title = models.ForeignKey(Title,
                             on_delete=models.CASCADE,
                             related_name='reviews')

    class Meta:
        app_label = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]
