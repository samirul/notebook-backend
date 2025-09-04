from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from BaseID.models import BaseIdModel
from accounts.models import User
from .task.task import execute_elastic_search_cmd

class CategoryNotes(BaseIdModel):
    title = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_category')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Note Category"

    def __str__(self):
        return str(self.title)
    

class Notes(BaseIdModel):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(CategoryNotes, on_delete= models.CASCADE, related_name= 'notes_category')
    note_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_note')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return str(self.title)
    

def exec_elastic_search_celery_task(*args, **kwargs):
    return execute_elastic_search_cmd.delay(*args, **kwargs)


@receiver(post_save, sender=CategoryNotes)
@receiver(post_save, sender=Notes)
def exec_elastic_search_celery_task_post_save(sender, instance, **kwargs):
    exec_elastic_search_celery_task()

@receiver(post_delete, sender=CategoryNotes)
@receiver(post_delete, sender=Notes)
def exec_elastic_search_celery_task_delete_save(sender, instance, **kwargs):
    exec_elastic_search_celery_task()

