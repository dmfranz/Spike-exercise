# Generated by Django 3.2.7 on 2021-10-08 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spikeapp', '0005_auto_20211008_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestform',
            name='response',
            field=models.CharField(default='Add Comment Here', max_length=500),
        ),
    ]