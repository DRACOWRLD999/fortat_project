# Generated by Django 4.2.3 on 2023-07-24 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_route_destination_alter_route_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MidwayStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='google_maps_link',
            field=models.URLField(default='https://www.google.com/maps', max_length=10000),
        ),
        migrations.AddField(
            model_name='route',
            name='midway_station',
            field=models.ManyToManyField(blank=True, to='api.midwaystation'),
        ),
    ]