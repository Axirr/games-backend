# Generated by Django 3.2.7 on 2021-09-15 20:06

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0022_alter_shogungame_isgameover'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeepSeaGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playersInGame', models.JSONField(default=dict)),
                ('currentTurn', models.IntegerField(default=1)),
                ('savedTreasure', models.JSONField(default=dict)),
                ('heldTreasures', models.JSONField(default=dict)),
                ('dice', models.JSONField(default=dict)),
                ('message', models.JSONField(default=dict)),
                ('points', models.JSONField(default=dict)),
                ('board', models.JSONField(default=dict)),
                ('isUp', models.JSONField(default=dict)),
                ('treasureBoard', models.JSONField(default=dict)),
                ('oxygenCounter', models.IntegerField(default=25)),
                ('remainingRounds', models.IntegerField(default=3)),
                ('maxPlayers', models.IntegerField(default=4)),
                ('doShuffle', models.BooleanField(default=True)),
                ('maxRemainingRounds', models.IntegerField(default=3)),
                ('buttonPhase', models.IntegerField(default=0)),
                ('maxOxygen', models.IntegerField(default=25)),
            ],
        ),
        migrations.AlterField(
            model_name='lovelettergame',
            name='message',
            field=django_mysql.models.ListCharField(models.CharField(max_length=100), default=['none', 'none', 'none', 'none', 'none', 'none'], max_length=606, size=6),
        ),
    ]