# Generated by Django 4.0 on 2022-12-01 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('resource_server', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'social_account',
            },
        ),
    ]
