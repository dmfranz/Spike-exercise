# Generated by Django 3.2.7 on 2021-10-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spikeapp', '0004_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_name', models.CharField(max_length=100)),
                ('landlord_name', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=500)),
                ('priority', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='RunningBalance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
