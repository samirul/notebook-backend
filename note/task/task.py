from celery import shared_task
from note.documents import CategoryNotesDocument

@shared_task(bind=True)
def delete_category_instance_from_elastic_search(self, instance_id):
    try:
        CategoryNotesDocument().get(id=instance_id).delete()
    except Exception as e:
        print(f"Something is wrong: {e}")