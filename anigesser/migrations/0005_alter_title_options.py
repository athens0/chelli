# Generated by Django 5.1.3 on 2025-01-25 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anigesser', '0004_title_members_screenshot'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-members'], 'verbose_name': 'Тайтл', 'verbose_name_plural': 'Тайтлы'},
        ),
    ]
