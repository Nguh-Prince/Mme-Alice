# Generated by Django 4.0.4 on 2022-06-06 13:31

from django.db import migrations, models
import django.db.models.deletion
import mysite.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('party', models.CharField(max_length=255)),
                ('statement', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VoteID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_code', models.CharField(default=mysite.models.generate_vote_code, max_length=255, unique=True)),
                ('idcard_num', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_made', models.DateTimeField(auto_now_add=True)),
                ('date_made', models.DateField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mysite.candidate')),
                ('voteid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mysite.voteid', unique=True)),
            ],
        ),
    ]
