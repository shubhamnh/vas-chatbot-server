# Generated by Django 3.1.5 on 2021-01-18 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='tclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.class', verbose_name='Class'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher'),
        ),
        migrations.AddField(
            model_name='semesterresult',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='marks',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course'),
        ),
        migrations.AddField(
            model_name='marks',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(to='users.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together={('weekday', 'timing', 'teacher', 'course', 'classroom', 'tclass', 'batch')},
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together={('student', 'course', 'semester')},
        ),
    ]