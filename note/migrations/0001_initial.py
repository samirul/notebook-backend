# Generated by Django 5.2 on 2025-05-13 14:35

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryNotes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category_title', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Note Category',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note_title', models.CharField(max_length=150)),
                ('note_text', models.TextField(max_length=20000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes_category', to='note.categorynotes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_note', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
    ]
