# Generated by Django 3.2.3 on 2021-05-27 14:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]