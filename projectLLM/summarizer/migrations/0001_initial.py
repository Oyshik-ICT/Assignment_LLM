# Generated by Django 5.1 on 2024-08-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropertySummary',
            fields=[
                ('property_id', models.IntegerField(
                    primary_key=True, serialize=False)),
                ('summary', models.TextField()),
            ],
        ),
    ]
