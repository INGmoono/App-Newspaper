# Generated by Django 5.0.7 on 2024-11-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_rename_comment_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/images/'),
        ),
    ]
