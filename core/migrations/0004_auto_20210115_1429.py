# Generated by Django 3.1.5 on 2021-01-15 13:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20210115_1233'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Oder',
            new_name='Order',
        ),
    ]
