# Generated by Django 2.2.4 on 2022-08-09 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210322_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='note',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('To-Do', 'To-Do'), ('In Progress', 'In Progress'), ('In Review', 'In Review'), ('Closed', 'Closed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('Issue', 'Issue'), ('Feature', 'Feature')], max_length=200, null=True),
        ),
    ]
