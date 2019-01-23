# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Dosen(models.Model):
    id = models.IntegerField(blank=True, null=True)
    nama_dosen = models.TextField(blank=True, null=True)  # This field type is a guess.
    username = models.TextField(blank=True, null=True)  # This field type is a guess.
    pass_field = models.TextField(db_column='pass', blank=True, null=True)  # Field renamed because it was a Python reserved word. This field type is a guess.
    prodi_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dosen'


class Fakultas(models.Model):
    fakultas_id = models.IntegerField(blank=True, null=True)
    nama_fakultas = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'fakultas'


class Prodi(models.Model):
    prodi_id = models.IntegerField(blank=True, null=True)
    nama_prodi = models.TextField(blank=True, null=True)  # This field type is a guess.
    jenjang = models.TextField(blank=True, null=True)  # This field type is a guess.
    fakultas_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prodi'
