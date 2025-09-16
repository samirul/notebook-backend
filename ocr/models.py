from django.db import models
from BaseID.models import BaseIdModel


class OCRModel(BaseIdModel):
    name = models.CharField(max_length=15)
    content = models.TextField()

    class Meta: # type: ignore
        verbose_name_plural = "OCR"

    def __str__(self) -> str:
        return str(self.name)