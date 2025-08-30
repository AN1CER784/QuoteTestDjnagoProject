from django.db import models


class Vote(models.Model):
    """
    Модель голоса.
    Связи:
    - Many-to-One с Quote (много голосов - одна цитата)
    - Many-to-One с User (много голосов - один пользователь)
    """
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = ((LIKE, 'Like'), (DISLIKE, 'Dislike'))
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quote', 'user')
