from django.db import models
from django.urls import get_resolver, URLResolver

class Help(models.Model):
    app_name = models.CharField(max_length=150)
    view_name = models.CharField(max_length=150)
    content = models.TextField()

    class Meta:
        verbose_name = "Help"
        verbose_name_plural = "Helps"
        unique_together = (("app_name", "view_name"),)
