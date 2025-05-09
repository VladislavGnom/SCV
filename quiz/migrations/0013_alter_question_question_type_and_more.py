# Generated by Django 4.2 on 2025-04-25 06:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_alter_testgroupaccess_available_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('SN', 'Один правильный ответ'), ('ML', 'Несколько правильных ответов'), ('TX', 'Текстовый'), ('TXA', 'Текстовый (auto)')], default='SN', max_length=3, verbose_name='Тип вопроса'),
        ),
        migrations.AlterField(
            model_name='testgroupaccess',
            name='available_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 4, 25, 6, 11, 56, 767165, tzinfo=datetime.timezone.utc), null=True, verbose_name='Доступен с'),
        ),
        migrations.AlterField(
            model_name='testgroupaccess',
            name='available_until',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 4, 26, 6, 11, 56, 767180, tzinfo=datetime.timezone.utc), null=True, verbose_name='Доступен до'),
        ),
    ]
