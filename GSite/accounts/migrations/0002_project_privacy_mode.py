# Generated by Django 4.2.7 on 2023-11-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='privacy_mode',
            field=models.BooleanField(default=True, verbose_name='Приватность'),
        ),
    ]