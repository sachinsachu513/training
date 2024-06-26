# Generated by Django 5.0.6 on 2024-06-01 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='combine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=15)),
                ('l_name', models.CharField(max_length=20)),
                ('email_id', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
