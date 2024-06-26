# Generated by Django 5.0.6 on 2024-05-27 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='fields',
            fields=[
                ('Auto_field', models.AutoField(primary_key=True, serialize=False)),
                ('Online', models.BooleanField()),
                ('date', models.DateField()),
                ('file', models.FileField(upload_to='')),
                ('foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.person')),
            ],
        ),
    ]
