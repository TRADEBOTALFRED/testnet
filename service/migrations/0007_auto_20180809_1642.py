# Generated by Django 2.0.7 on 2018-08-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20180809_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairdata',
            name='volume',
            field=models.DecimalField(decimal_places=6, max_digits=12),
        ),
    ]
