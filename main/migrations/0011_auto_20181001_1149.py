# Generated by Django 2.1.1 on 2018-10-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20181001_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='away_team_score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='matches',
            name='home_team_score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
