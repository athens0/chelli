# Generated by Django 5.1.3 on 2025-01-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anigesser', '0006_title_description_character_screenshots_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Студия',
                'verbose_name_plural': 'Студии',
            },
        ),
        migrations.AddField(
            model_name='title',
            name='studio',
            field=models.ManyToManyField(related_name='titles', to='anigesser.studio', verbose_name='Студии'),
        ),
    ]
