# Generated by Django 2.1.5 on 2019-02-18 18:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0002_auto_20190208_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='protectedresource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='protectedresource',
            name='file',
            field=models.FileField(default=None, null=True, upload_to='uploads/'),
        ),
    ]