# Generated by Django 3.1 on 2020-09-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_image_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_attachment',
            field=models.ImageField(blank=True, upload_to='post_attachments'),
        ),
    ]
