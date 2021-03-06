# Generated by Django 3.2.3 on 2021-07-06 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=70)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.CharField(default='Unknown', max_length=50)),
                ('province', models.CharField(default='Unknown', max_length=50)),
                ('address', models.CharField(default='Unknown', max_length=100)),
                ('nodeType', models.CharField(choices=[('S', 'Station'), ('A', 'Airport')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='RESTApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('BaseUrl', models.CharField(max_length=50)),
                ('APIKey', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureDate', models.DateTimeField()),
                ('arrivalDate', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('price', models.FloatField()),
                ('arrivalNode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivalNode', to='app.node')),
                ('departureNode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departureNode', to='app.node')),
            ],
        ),
        migrations.CreateModel(
            name='skyscannerTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlPay', models.URLField(max_length=1500)),
                ('airlineName', models.CharField(max_length=50)),
                ('airlineUrlImage', models.CharField(max_length=50)),
                ('trip', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skyscannerTrip', to='app.trip')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('PartToaddToBaseUrl', models.CharField(max_length=200)),
                ('funcToExtractDataFromJsonName', models.CharField(max_length=100)),
                ('ParamsOrDataDictStructure', models.JSONField()),
                ('typeRequests', models.CharField(choices=[('GET', 'Get'), ('POST', 'Post')], max_length=5)),
                ('headers', models.JSONField(blank=True, null=True)),
                ('RApi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='app.restapi')),
            ],
        ),
        migrations.CreateModel(
            name='busOrTrainTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(choices=[('T', 'Train'), ('B', 'Bus')], max_length=5)),
                ('trip', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='busOrTrainTrip', to='app.trip')),
            ],
        ),
        migrations.CreateModel(
            name='blablaTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(max_length=150)),
                ('departureCity', models.CharField(max_length=30)),
                ('departureAddress', models.CharField(max_length=30)),
                ('departureLatitude', models.FloatField()),
                ('departureLongitude', models.FloatField()),
                ('arrivalCity', models.CharField(max_length=30)),
                ('arrivalAddress', models.CharField(max_length=30)),
                ('arrivalLatitude', models.FloatField()),
                ('arrivalLongitude', models.FloatField()),
                ('trip', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blablaTrip', to='app.trip')),
            ],
        ),
    ]
