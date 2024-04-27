# Generated by Django 4.2.11 on 2024-04-25 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=150)),
                ('user_name', models.CharField(max_length=50)),
                ('user_last_name', models.CharField(max_length=50)),
                ('user_occupation_name', models.CharField(max_length=80)),
                ('user_location_name', models.CharField(max_length=150)),
                ('signup_date', models.CharField(max_length=10)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('last_update_date', models.CharField(blank=True, default='P', max_length=50)),
            ],
        ),
    ]
