# Generated by Django 3.0.6 on 2020-08-17 10:57

from django.db import migrations, models
import django.db.models.deletion
import weatherapp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0006_auto_20200505_0252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='forecast',
            name='citydata',
            field=weatherapp.fields.JSONField(default=''),
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loadingtime', models.DateTimeField(auto_now_add=True)),
                ('weatherdata', weatherapp.fields.JSONField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.City')),
            ],
            options={
                'ordering': ['-loadingtime'],
            },
        ),
    ]
