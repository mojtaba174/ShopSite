# Generated by Django 4.2.20 on 2025-03-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_icon_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='icon',
        ),
        migrations.AddField(
            model_name='brand',
            name='icon',
            field=models.ImageField(default='static/default.png', upload_to='', verbose_name='آیکون'),
        ),
    ]
