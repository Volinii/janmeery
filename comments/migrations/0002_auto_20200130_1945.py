# Generated by Django 2.2.9 on 2020-01-30 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_time'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]