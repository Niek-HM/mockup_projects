# Generated by Django 3.2.9 on 2023-12-31 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_archive_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
            ],
        ),
        migrations.AddField(
            model_name='archive',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='archive',
            name='title',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='archive',
            name='tag',
            field=models.ManyToManyField(to='main.Tag'),
        ),
    ]
