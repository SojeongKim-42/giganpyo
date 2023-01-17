# Generated by Django 4.0.3 on 2023-01-13 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tableapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(blank=True, default='시간표', max_length=100),
        ),
        migrations.AlterField(
            model_name='table',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_user', to=settings.AUTH_USER_MODEL),
        ),
    ]