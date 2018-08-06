# Generated by Django 2.0.7 on 2018-07-31 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_market_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairdata',
            name='close_price',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pairdata',
            name='high_price',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pairdata',
            name='low_price',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pairdata',
            name='open_price',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pairdata',
            name='volume',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
    ]
