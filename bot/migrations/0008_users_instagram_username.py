# Generated by Django 4.0.5 on 2022-06-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_usertypecategory_alter_messages_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='instagram_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]