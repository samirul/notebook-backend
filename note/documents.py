from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import CategoryNotes, Notes


@registry.register_document
class CategoryNotesDocument(Document):
    user = fields.KeywordField(attr='user_id')
    class Index:
        name = "categorynotes"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    
    class Django:
        model = CategoryNotes
        fields= ["title"]

@registry.register_document
class NotesDocument(Document):
    user = fields.KeywordField(attr='user_id')
    class Index:
        name = "notes"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    
    class Django:
        model = Notes
        fields = ["title"]