from django.db import models
from accounts.models import User
from BaseID.models import BaseIdModel
from custom_exceptions.exceptions import NotFoundRequiredTypeFileUploadException


class OCRFIleUpload(BaseIdModel):
    title = models.CharField(max_length=255)
    file_upload = models.FileField(upload_to='uploaded_pdf')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_file_upload')
    objects = models.Manager()

    class Meta: # type: ignore
        verbose_name_plural = "OCR File Upload"

    def save(self, *args, **kwargs):
        if not self.file_upload.name.endswith(('.pdf', '.png', '.jpg', 'jpeg')):
            raise NotFoundRequiredTypeFileUploadException ("File must be pdf, png, jpg or jpeg.")
        self.title = self.file_upload.name
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)


class OCRModel(BaseIdModel):
    name = models.CharField(max_length=15)
    content = models.TextField()

    class Meta: # type: ignore
        verbose_name_plural = "OCR"

    def __str__(self) -> str:
        return str(self.name)