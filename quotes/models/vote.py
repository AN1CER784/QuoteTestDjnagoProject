from django.db import models


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = ((LIKE, 'Like'), (DISLIKE, 'Dislike'))
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quote', 'user')
