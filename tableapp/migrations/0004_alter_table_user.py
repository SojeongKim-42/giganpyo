# Generated by Django 4.0.3 on 2023-01-13 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tableapp', '0003_alter_table_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_user', to=settings.AUTH_USER_MODEL),
        ),
    ]