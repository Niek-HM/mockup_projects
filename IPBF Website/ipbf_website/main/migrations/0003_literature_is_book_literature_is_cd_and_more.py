# Generated by Django 4.2.5 on 2023-09-28 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_autors_literature_authors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='literature',
            name='is_book',
            field=models.BooleanField(default=False, verbose_name='Book'),
        ),
        migrations.AddField(
            model_name='literature',
            name='is_cd',
            field=models.BooleanField(default=False, verbose_name='CD'),
        ),
        migrations.AddField(
            model_name='literature',
            name='is_video',
            field=models.BooleanField(default=False, verbose_name='Video'),
        ),
    ]
