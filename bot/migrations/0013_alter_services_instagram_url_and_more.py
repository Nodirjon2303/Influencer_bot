# Generated by Django 4.0.5 on 2022-06-19 05:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='instagram_url',
            field=models.CharField(default=django.utils.timezone.now, max_length=125),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='services',
            name='lefquantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='services',
            name='quantity',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='services',
            name='status',
            field=models.CharField(choices=[('progress', 'Progress'), ('done', 'Finished')], default='progress', max_length=125),
        ),
    ]
