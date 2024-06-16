# Generated by Django 5.0.6 on 2024-05-27 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_artist_artist1'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=15)),
                ('course', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.IntegerField()),
                ('staff_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.teacher')),
            ],
        ),
    ]
