# Generated by Django 5.1.3 on 2024-12-04 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0017_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
