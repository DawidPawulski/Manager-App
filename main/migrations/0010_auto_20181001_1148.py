# Generated by Django 2.1.1 on 2018-10-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20180930_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='away_team_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='home_team_score',
            field=models.IntegerField(null=True),
        ),
    ]
