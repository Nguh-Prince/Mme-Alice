# Generated by Django 4.0.4 on 2022-06-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_alter_vote_voteid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteid',
            name='idcard_num',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]