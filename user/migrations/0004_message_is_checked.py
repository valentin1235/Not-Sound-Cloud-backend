# Generated by Django 3.0.3 on 2020-03-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200316_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
