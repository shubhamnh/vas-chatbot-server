# Generated by Django 3.1.4 on 2021-02-11 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210205_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intereststatus',
            name='interest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='users.interest'),
        ),
    ]