# Generated by Django 4.2.11 on 2024-05-12 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportevent',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stations.appuser'),
        ),
    ]