# Generated by Django 4.2.5 on 2023-09-28 20:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_page_editabletext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editabletext',
            name='page',
        ),
        migrations.AddField(
            model_name='editabletext',
            name='url',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]