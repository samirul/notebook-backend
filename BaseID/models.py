"""
    Created a abstract model.
"""
import uuid
from django.db import models

class BaseIdModel(models.Model):
    """A abstract model is a model for inheriting these fields only by other models.
    BaseIdModel will not migrate on the database by itself for being abstract.
    It is only for inheriting repeated fields by other models that will migrate
    to the database.

    Args:
        models (Modules): Django Model.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class in django model is for changing model behavior."""
        abstract = True
