# Generated by Django 4.2.7 on 2023-11-23 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyms', '0003_question_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
