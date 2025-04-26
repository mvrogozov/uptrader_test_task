from django.db import models


class Menu(models.Model):
    menu = models.JSONField(
        null=True,
        blank=True,
        verbose_name='меню'
    )
