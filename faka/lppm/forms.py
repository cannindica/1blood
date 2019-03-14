from django import forms
from .models import Dosen, Penelitian, Pengabdian
from django.contrib.auth.models import User
# from upload_validator import FileTypeValidator


class PenelitianForm(forms.ModelForm):
	class Meta:
		model = Penelitian
		fields = (
			'judul', 'abstrak', 'tahun', 'lokasi', 'file', 'lokasi_id',
			)
		# widgets = {
		# 	'tahun': forms.TextInput(attrs={'type': 'number', 'placeholder': ""}),
		# }


class PengabdianForm(forms.ModelForm):
	class Meta:
		model = Pengabdian
		fields = (
			'judul', 'tahun', 'lokasi', 'file', 'abstrak', 'lokasi_id',
			)
		# widgets = {
		# 	'tahun': forms.TextInput(attrs={'type': 'number', 'placeholder': ""}),
		# }