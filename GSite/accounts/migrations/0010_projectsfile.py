# Generated by Django 4.2.7 on 2023-12-01 22:49

import accounts.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_profile_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=accounts.utils.get_projects_files_path, verbose_name='Файл проекта')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.project', verbose_name='Проект')),
            ],
        ),
    ]
