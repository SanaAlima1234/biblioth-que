# Generated by Django 5.1.6 on 2025-05-23 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='valide',
            field=models.BooleanField(default=False),
        ),
    ]
