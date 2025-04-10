# Generated by Django 4.2 on 2024-10-20 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_remove_customuser_login_subjectchildren'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=600)),
                ('question_group', models.IntegerField(default=0)),
                ('question_points', models.IntegerField()),
                ('question_type', models.IntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectmain')),
                ('subject_child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectchildren')),
                ('subject_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.subjectparents')),
            ],
        ),
    ]
