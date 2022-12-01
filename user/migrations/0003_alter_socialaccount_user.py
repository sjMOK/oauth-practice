# Generated by Django 4.0 on 2022-12-01 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_socialaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='social_account', serialize=False, to='user.user'),
        ),
    ]
