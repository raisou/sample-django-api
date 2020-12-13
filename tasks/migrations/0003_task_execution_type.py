# Generated by Django 3.1.4 on 2020-12-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20201210_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='execution_type',
            field=models.CharField(choices=[('Heavy', 'Tâche à exécution longue'), ('Light', 'Tâche à exécution rapide'), ('Random', 'Tâche à exécution à durée variable')], default='async', editable=False, max_length=30),
            preserve_default=False,
        ),
    ]
