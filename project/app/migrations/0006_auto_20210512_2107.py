# Generated by Django 3.2 on 2021-05-12 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_urlpago_skyscannertrip_urlpay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skyscannertrip',
            old_name='AirlineName',
            new_name='airlineName',
        ),
        migrations.RenameField(
            model_name='skyscannertrip',
            old_name='AirlineUrlImage',
            new_name='airlineUrlImage',
        ),
    ]