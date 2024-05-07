from django.db import models


class AbstractDateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True
