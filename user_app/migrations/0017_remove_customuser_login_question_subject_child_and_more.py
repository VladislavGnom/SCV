# Generated by Django 4.2 on 2024-10-23 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0016_remove_customuser_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subject_child',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectchildren'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject_parent',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectparents'),
        ),
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectmain'),
        ),
    ]