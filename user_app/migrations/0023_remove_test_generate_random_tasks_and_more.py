# Generated by Django 4.2 on 2024-11-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0022_test_generate_random_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='generate_random_tasks',
        ),
        migrations.AddField(
            model_name='test',
            name='generate_random_order_tasks',
            field=models.BooleanField(default=False, verbose_name='Генерировать вопросы в перемешку'),
        ),
    ]
