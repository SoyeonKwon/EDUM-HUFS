# Generated by Django 2.1.2 on 2018-11-07 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trash', models.BooleanField()),
            ],
        ),
    ]
