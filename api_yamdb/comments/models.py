from django.contrib.auth import get_user_model
from django.db import models

from reviews.models import Review

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments"
                               )
    review = models.ForeignKey(Review,
                            on_delete=models.CASCADE,
                            related_name="comments"
                            )
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("Дата добавления",
                                   auto_now_add=True,
                                   db_index=True
                                   )

    class Meta:
        app_label ='comments'
