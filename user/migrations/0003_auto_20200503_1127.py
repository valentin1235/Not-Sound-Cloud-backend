# Generated by Django 3.0.3 on 2020-05-03 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200319_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageNumbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'message_numbers',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='message_numbers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.MessageNumbers'),
        ),
    ]
