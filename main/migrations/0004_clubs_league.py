# Generated by Django 2.1.1 on 2018-09-30 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180930_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubs',
            name='league',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Leagues'),
            preserve_default=False,
        ),
    ]
