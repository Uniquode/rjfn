# Generated by Django 3.1.2 on 2020-10-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_testimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmspage',
            name='display_banner',
            field=models.BooleanField(default=True),
        ),
    ]