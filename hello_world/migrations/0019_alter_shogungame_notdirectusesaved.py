# Generated by Django 3.2.6 on 2021-09-01 21:24

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0018_remove_shogungame_buycards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shogungame',
            name='notDirectUseSaved',
            field=django_mysql.models.ListCharField(models.CharField(max_length=10), default=['0', '0', '0', '0', '0', '0'], max_length=66, size=6),
        ),
    ]