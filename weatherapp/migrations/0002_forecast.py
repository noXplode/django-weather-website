# Generated by Django 3.0.3 on 2020-04-12 13:04

from django.db import migrations, models
import django.db.models.deletion
import weatherapp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loadingtime', models.DateTimeField(auto_now_add=True)),
                ('forecastdata', weatherapp.fields.JSONField()),
                ('cityid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.City')),
            ],
        ),
    ]