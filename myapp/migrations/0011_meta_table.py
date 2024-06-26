# Generated by Django 5.0.6 on 2024-05-31 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_q_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='meta_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Metas',
                'db_table': 'Meta',
                'ordering': ['-price'],
                'unique_together': {('name', 'created_at')},
            },
        ),
    ]
