# Generated by Django 3.2.6 on 2021-09-01 15:12

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0011_alter_lovelettergame_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shogun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dice', django_mysql.models.ListCharField(models.CharField(max_length=20), default=['none', 'none', 'none', 'none', 'none', 'none'], max_length=126, size=6)),
                ('notDirectUseDice', django_mysql.models.ListCharField(models.CharField(max_length=1), default=['0', '0', '0', '0', '0', '0'], max_length=12, size=6)),
                ('notDirectUsePlayersInGame', django_mysql.models.ListCharField(models.CharField(max_length=1), default=['1', '2', '3', '4'], max_length=12, size=6)),
                ('currentTurn', models.IntegerField(default=1)),
                ('notDirectUseHands', models.JSONField(default={'hands': [[], [], [], []]})),
            ],
        ),
    ]