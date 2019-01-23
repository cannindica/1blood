# Generated by Django 2.1.2 on 2019-01-17 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lppm.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnggotaPenelitian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('1', 'Ketua'), ('2', 'Anggota')], max_length=1)),
                ('nama', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Dosen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Fakultas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fakultas_id', models.CharField(max_length=2)),
                ('fakultas_nama', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Penelitian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=lppm.models.upload_penelitian)),
                ('status', models.BooleanField(default=False)),
                ('tahun', models.CharField(max_length=5)),
                ('judul', models.CharField(max_length=120)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lokasi', models.CharField(max_length=120)),
                ('abstrak', models.TextField()),
                ('dosen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lppm.Dosen')),
            ],
        ),
        migrations.CreateModel(
            name='Prodi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodi_id', models.CharField(max_length=2)),
                ('prodi_nama', models.CharField(max_length=120)),
                ('fakultas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lppm.Fakultas')),
            ],
        ),
        migrations.CreateModel(
            name='Validatori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dosen',
            name='prodi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lppm.Prodi'),
        ),
        migrations.AddField(
            model_name='dosen',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='anggotapenelitian',
            name='penelitian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lppm.Penelitian'),
        ),
    ]