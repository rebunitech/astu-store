from django.db import models
from django.urls import URLResolver, get_resolver


class Help(models.Model):
    app_name = models.CharField(max_length=150)
    view_name = models.CharField(max_length=150)
    is_visible = models.BooleanField(default=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Help"
        verbose_name_plural = "Helps"
        unique_together = (("app_name", "view_name"),)
