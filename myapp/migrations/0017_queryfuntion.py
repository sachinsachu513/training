# Generated by Django 5.0.6 on 2024-06-06 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_green11_spartan_pcc_green11_young_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='queryfuntion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.DecimalField(decimal_places=2, max_digits=10)),
                ('y', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
