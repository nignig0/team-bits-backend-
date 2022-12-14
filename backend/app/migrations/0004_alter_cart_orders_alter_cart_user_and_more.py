# Generated by Django 4.0.4 on 2022-10-21 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(blank=True, to='app.order'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='business',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.business'),
        ),
    ]
