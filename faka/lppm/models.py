from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os


def upload_penelitian(instance, filename):
	return '/'.join(['penelitian', instance.dosen.user.username, filename])


def upload_pengabdian(instance, filename):
	return '/'.join(['pengabdian', instance.dosen.user.username, filename])


def upload_poto(instance, filename):
	return '/'.join(['foto', instance.dosen.user.username, filename])


class Fakultas(models.Model):
	fakultas_id = models.CharField(max_length=2, blank=False)
	fakultas_nama = models.CharField(max_length=35, blank=False)

	def __str__(self):
		return "{0} - {1}".format(self.fakultas_id, self.fakultas_nama)


class Prodi(models.Model):
	fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE)
	prodi_id = models.CharField(max_length=2, blank=False)
	prodi_nama = models.CharField(max_length=120, blank=False)

	def __str__(self):
		return "{0} - {1}".format(self.prodi_id, self.prodi_nama)


class Dosen(models.Model):
	prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	foto = models.ImageField(
		upload_to=upload_poto,
		default='default.jpg',
	)

	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.user.first_name)


class Penelitian(models.Model):
	dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
	file = models.FileField(
		upload_to=upload_penelitian,
		blank=False,
		null=False,
	)
	status = models.BooleanField(default=False)
	tahun = models.CharField(max_length=5, blank=False)
	judul = models.CharField(max_length=120, blank=False)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	lokasi = models.CharField(max_length=120, blank=False)
	abstrak = models.TextField(blank=False)



@receiver(models.signals.post_delete, sender=Penelitian)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.file:
		if os.path.isfile(instance.file.path):
			os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Penelitian)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = sender.objects.get(pk=instance.pk).file
	except sender.DoesNotExist:
		return False
	new_file = instance.file 
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)


class AnggotaPenelitian(models.Model):
	penelitian = models.ForeignKey(Penelitian, on_delete=models.CASCADE)
	LEVEL = (
		("1", "Ketua"),
		("2", "Anggota"),
	)
	level = models.CharField(
		max_length=1,
		choices=LEVEL,
	)
	nama = models.CharField(max_length=120, blank=False)


#############################################################################################################################

class Pengabdian(models.Model):
	dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
	file = models.FileField(
		upload_to=upload_pengabdian,
		blank=False,
		null=False,
	)
	status = models.BooleanField(default=False)
	tahun = models.CharField(max_length=5, blank=False)
	judul = models.CharField(max_length=120, blank=False)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	lokasi = models.CharField(max_length=120, blank=False)
	abstrak = models.TextField(blank=False)



@receiver(models.signals.post_delete, sender=Pengabdian)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.file:
		if os.path.isfile(instance.file.path):
			os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Pengabdian)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False
	try:
		old_file = sender.objects.get(pk=instance.pk).file
	except sender.DoesNotExist:
		return False
	new_file = instance.file 
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)


class AnggotaPengabdian(models.Model):
	pengabdian = models.ForeignKey(Pengabdian, on_delete=models.CASCADE)
	LEVEL = (
		("1", "Ketua"),
		("2", "Anggota"),
	)
	level = models.CharField(
		max_length=1,
		choices=LEVEL,
	)
	nama = models.CharField(max_length=120, blank=False)


class Validatori(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)