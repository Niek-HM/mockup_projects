# Generated by Django 4.2.5 on 2023-09-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_editabletext_page_editabletext_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editabletext',
            name='url',
            field=models.CharField(max_length=24),
        ),
    ]
