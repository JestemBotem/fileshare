# Generated by Django 2.1.5 on 2019-02-08 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='protectedresource',
            name='file',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='protectedresource',
            name='uri',
            field=models.TextField(default=None, null=True),
        ),
    ]