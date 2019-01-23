from django.db import models
from django.contrib.auth.models import User
# from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
import os


def upload_penelitian(instance, filename):
	return '/'.join(['penelitian', instance.dosen.user.username, filename])


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

	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.user.first_name)


class Penelitian(models.Model):
	dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
	# dosen_id = models.IntegerField(blank=False)
	# dosen_nama = models.CharField(max_length=75, blank=False)
	# prodi = models.IntegerField(blank=False)
	# prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE, related_name='prodi_fk')
	file = models.FileField( # file must .pdf/.word
		upload_to=upload_penelitian,
		blank=False,
		null=False,
		# validators=[FileExtensionValidator(['pdf'])],
	)
	status = models.BooleanField(default=False) # False = Not Accepted, True = Accepted
	# validasi_dsn = models.CharField(max_length=120, blank=True)
	# timestamp_validasi = models.DateTimeField()
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


class Validatori(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


# note : API login unira itu dapet apa aja?? feedback data if success login??