# Generated by Django 3.2.18 on 2023-03-08 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_alter_roadsegment_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadsegment',
            name='length',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
