# Generated by Django 3.0.2 on 2020-01-26 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_delete_tabla_intereses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tabla_intereses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ss', models.IntegerField()),
                ('ep', models.IntegerField()),
                ('v', models.IntegerField()),
                ('ap', models.IntegerField()),
                ('ms', models.IntegerField()),
                ('og', models.IntegerField()),
                ('ct', models.IntegerField()),
                ('ci', models.IntegerField()),
                ('mc', models.IntegerField()),
                ('al', models.IntegerField()),
                ('p_ss', models.IntegerField()),
                ('p_ep', models.IntegerField()),
                ('p_v', models.IntegerField()),
                ('p_ap', models.IntegerField()),
                ('p_ms', models.IntegerField()),
                ('p_og', models.IntegerField()),
                ('p_ct', models.IntegerField()),
                ('p_ci', models.IntegerField()),
                ('p_mc', models.IntegerField()),
                ('p_al', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
