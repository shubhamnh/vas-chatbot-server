# Generated by Django 3.1.4 on 2021-02-14 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210214_0822'),
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupnotification',
            name='visited',
        ),
        migrations.AlterField(
            model_name='groupnotification',
            name='nclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.class', verbose_name='Class'),
        ),
    ]
