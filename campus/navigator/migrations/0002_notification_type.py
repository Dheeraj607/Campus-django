# Generated by Django 5.1.4 on 2025-01-10 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.IntegerField(null=True),
        ),
    ]