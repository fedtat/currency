# Generated by Django 4.0.3 on 2022-05-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]
