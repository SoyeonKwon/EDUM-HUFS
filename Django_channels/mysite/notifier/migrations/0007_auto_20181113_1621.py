# Generated by Django 2.1.2 on 2018-11-13 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0006_detections'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Detections',
        ),
        migrations.AddField(
            model_name='camera',
            name='instrusion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='camera',
            name='trash',
            field=models.BooleanField(default=False),
        ),
    ]
