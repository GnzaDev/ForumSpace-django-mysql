# Generated by Django 5.1.1 on 2024-10-22 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0004_notificacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
    ]
