from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api.validators import validate_year


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Дата публикации',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category, 
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
    )
    genre = models.ManyToManyField(
        Genre, 
        verbose_name='Жанр'
        related_name='titles',
        blank=True, 
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


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
