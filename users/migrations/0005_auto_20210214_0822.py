# Generated by Django 3.1.4 on 2021-02-14 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210211_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intereststatus',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='users.student'),
        ),
    ]