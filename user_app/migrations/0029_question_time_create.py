# Generated by Django 4.2 on 2024-11-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0028_alter_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]