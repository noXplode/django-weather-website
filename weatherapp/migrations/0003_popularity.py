# Generated by Django 3.0.5 on 2020-04-21 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0002_forecast'),
    ]

    operations = [
        migrations.CreateModel(
            name='Popularity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickeddate', models.DateTimeField(auto_now_add=True)),
                ('cityid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.City')),
            ],
        ),
    ]
