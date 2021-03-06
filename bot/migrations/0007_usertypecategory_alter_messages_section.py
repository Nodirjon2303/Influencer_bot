# Generated by Django 4.0.5 on 2022-06-15 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_delete_button_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTypeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, null=True)),
                ('name_ar', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='messages',
            name='section',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bot.sections'),
        ),
    ]
