from django.db import models
from BaseID.models import BaseIdModel
from accounts.models import User

class CategoryNotes(BaseIdModel):
    category_title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_category')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Note Category"

    def __str__(self):
        return str(self.category_title)
    

class Notes(BaseIdModel):
    note_title = models.CharField(max_length=150)
    category = models.ForeignKey(CategoryNotes, on_delete= models.CASCADE, related_name= 'notes_category')
    note_text = models.TextField(max_length=20000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_note')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return str(self.note_title)
