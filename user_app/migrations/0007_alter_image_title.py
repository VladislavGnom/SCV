# Generated by Django 4.2 on 2024-09-07 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_remove_test_current_attempts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
