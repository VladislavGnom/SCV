# Generated by Django 5.0.7 on 2024-07-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_test_task_numbers_test_task_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='count_right_answers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]