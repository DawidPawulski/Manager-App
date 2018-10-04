# Generated by Django 2.1.1 on 2018-09-30 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180930_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerShirtNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Players')),
            ],
        ),
        migrations.AddField(
            model_name='matches',
            name='league',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.Leagues'),
            preserve_default=False,
        ),
    ]
