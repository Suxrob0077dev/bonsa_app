# Generated by Django 5.2 on 2025-05-15 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
