# Generated by Django 4.2 on 2024-11-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0029_question_time_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(upload_to='imgs'),
        ),
    ]