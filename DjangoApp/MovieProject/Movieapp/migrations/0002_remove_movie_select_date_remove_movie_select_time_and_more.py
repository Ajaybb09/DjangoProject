# Generated by Django 4.0.2 on 2022-02-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movieapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='select_date',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='select_time',
        ),
        migrations.AddField(
            model_name='movie',
            name='Price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
