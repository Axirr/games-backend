# Generated by Django 3.2.6 on 2021-09-01 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0014_auto_20210901_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shogun',
            old_name='notDirectUseDice',
            new_name='notDirectUseSaved',
        ),
    ]
