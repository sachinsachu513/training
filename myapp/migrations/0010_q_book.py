# Generated by Django 5.0.6 on 2024-05-30 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='q_book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('date', models.IntegerField()),
            ],
        ),
    ]