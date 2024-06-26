# Generated by Django 5.0.6 on 2024-06-05 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restapi', '0008_user_new_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='schoolname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=20)),
                ('school_location', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='studentdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('age', models.IntegerField()),
                ('student_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restapi.schoolname')),
            ],
        ),
    ]
