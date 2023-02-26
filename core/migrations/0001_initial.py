# Generated by Django 3.2.2 on 2021-05-27 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadosDemograficos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('populacao', models.IntegerField()),
                ('area', models.IntegerField()),
                ('estado', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=10)),
            ],
            options={
                'db_table': 'dadosdemograficos',
            },
        ),
        migrations.CreateModel(
            name='Doencas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('origem', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'doencas',
            },
        ),
        migrations.CreateModel(
            name='LocaisVisitados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=10)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=10)),
            ],
            options={
                'db_table': 'locaisvisitados',
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('cidade', models.CharField(max_length=100)),
                ('id_facebook', models.CharField(max_length=15)),
                ('locaisvisitados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuarios', to='core.locaisvisitados')),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Relatorios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casos', models.IntegerField()),
                ('dadosdemograficos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Relatorios', to='core.dadosdemograficos')),
                ('doenca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Relatorios', to='core.doencas')),
            ],
            options={
                'db_table': 'relatorios',
            },
        ),
        migrations.CreateModel(
            name='Cruzamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doenca_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.doencas')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usuarios')),
            ],
            options={
                'unique_together': {('usuario_id', 'doenca_id')},
            },
        ),
    ]
