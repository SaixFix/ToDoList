# Generated by Django 4.1.7 on 2023-04-05 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_alter_goalcomment_goal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalcomment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
