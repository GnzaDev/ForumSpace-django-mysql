# Generated by Django 5.1.1 on 2024-10-18 02:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0003_remove_categoria_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('leida', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacion_autor', to=settings.AUTH_USER_MODEL)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.tema')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
