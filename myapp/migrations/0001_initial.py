# Generated by Django 5.0.6 on 2024-05-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_no', models.IntegerField()),
                ('emp_name', models.CharField(max_length=10)),
                ('emp_adress', models.CharField(max_length=10)),
            ],
        ),
    ]
