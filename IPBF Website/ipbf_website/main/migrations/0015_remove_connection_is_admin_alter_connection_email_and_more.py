# Generated by Django 4.2.5 on 2024-01-15 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_literaturetag_literature_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='connection',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='connection',
            name='phone',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
