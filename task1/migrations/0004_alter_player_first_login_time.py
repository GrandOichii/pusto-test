# Generated by Django 5.1.1 on 2024-09-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='first_login_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
