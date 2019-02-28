from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View
from django.http import JsonResponse
import datetime
from notifications.signals import notify
from . models import Fakultas, Prodi, Dosen, Penelitian, AnggotaPenelitian, Validatori, Pengabdian, AnggotaPengabdian
import requests, json
from .forms import PenelitianForm, PengabdianForm
from django.contrib.contenttypes.models import ContentType



def awal(request):
	awal = True
	try:
		user = get_object_or_404(User, pk=request.user.pk)
	except:
		user = ""
	statistik_penelitian = True
	fakultas = Fakultas.objects.all()
	penelitian = {}
	pengabdian = {}
	for i in fakultas:
		penelitian[i.fakultas_nama] = {}
		pengabdian[i.fakultas_nama] = {}
		prodi = Prodi.objects.filter(fakultas=i)
		for j in prodi:
			penelitian[i.fakultas_nama][j.prodi_nama] = len(Penelitian.objects.filter(dosen__prodi=j).exclude(status=False))
			pengabdian[i.fakultas_nama][j.prodi_nama] = len(Pengabdian.objects.filter(dosen__prodi=j).exclude(status=False))
	context = {
		'user': user,
		'statistik_penelitian': statistik_penelitian,
		'penelitian': penelitian,
		'pengabdian': pengabdian,
	}
	return render(request, '1blood-2/index.html', context)


def login_dosen(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		data_api = {
			'username': username,
			'password': password,
		}
		validation_api = requests.post(url='https://api.unira.ac.id/v1/token', data=data_api)
		if validation_api.status_code != 201:
			messages.error(request, "Login Gagal !!!")
			return redirect('lppm:masuk')
		else:
			validate_user = authenticate(request, username=username, password=password)
			if validate_user is not None:
				login(request, validate_user)
				return redirect('lppm:home')
			else:
				d_validation_api = json.loads(validation_api.content.decode('utf-8'))
				token = d_validation_api["data"]["attributes"]["access"]
				headers = {
					'Content-Type': 'application/json', 
					'Authorization': 'Bearer {0}'.format(token),
				}
				validation_api_2 = requests.get('https://api.unira.ac.id/v1/saya', headers=headers)
				if validation_api_2.status_code != 200:
					messages.error("Login Gagal !!!")
					return redirect('lppm:masuk')
				d_validation_api_2 = json.loads(validation_api_2.content.decode('utf-8'))
				prodi_instance = get_object_or_404(Prodi, prodi_id=d_validation_api_2["data"]["attributes"]["prodi"])
				user_instance = User.objects.create_user(username=username, password=password)
				user_instance.first_name = d_validation_api_2["data"]["attributes"]["nama"]
				user_instance.save()
				dosen_instance = Dosen.objects.create(prodi=prodi_instance, user=user_instance)
				validate_user_2 = authenticate(request, username=username, password=password)
				if validate_user_2 is not None:
					login(request, validate_user_2)
					return redirect('lppm:home')
	return render(request, '1blood-2/login.html', {})


def penelitian_statistik(request):
	try:
		user = get_object_or_404(User, pk=request.user.pk)
	except:
		user = ""
	statistik_penelitian = True
	fakultas = Fakultas.objects.all()
	penelitian = {}
	for i in fakultas:
		penelitian[i.fakultas_nama] = {}
		prodi = Prodi.objects.filter(fakultas=i)
		for j in prodi:
			penelitian[i.fakultas_nama][j.prodi_nama] = len(Penelitian.objects.filter(dosen__prodi=j).exclude(status=False))
	context = {
		'user': user,
		'statistik_penelitian': statistik_penelitian,
		'penelitian': penelitian,
	}
	return render(request, '1blood-2/index.html', context)


class PenelitianChart(APIView):
	authentication_classes = []
	permission_classes = []
	
	def get(self, request, format=None):
		labels = []
		default_items = []
		tahun = str(datetime.datetime.now().year)
		for i in range(14):
			labels.append(int(tahun) - i)
		for i in labels:
			default_items.append(len(Penelitian.objects.filter(tahun=str(i)).exclude(status=False)))
		labels.reverse() # list tahun
		default_items.reverse() # list penelitian
		data = {
			"labels": labels,
			"default": default_items,
		}
		return Response(data)


class PenelitianProdiChart(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		prodi = Prodi.objects.get(prodi_nama=request.GET.get('faka'))
		labels = []
		default_items = []
		tahun = str(datetime.datetime.now().year)
		for i in range(14):
			labels.append(int(tahun) - i)
		for i in labels:
			default_items.append(len(Penelitian.objects.filter(dosen__prodi=prodi).filter(tahun=str(i)).exclude(status=False)))
		labels.reverse() # list tahun
		default_items.reverse() # list penelitian
		data = {
			"labels": labels,
			"default": default_items,
		}
		return Response(data)


def pengabdian_statistik(request):
	try:
		user = get_object_or_404(User, pk=request.user.pk)
	except:
		user = ""
	statistik_pengabdian = True
	fakultas = Fakultas.objects.all()
	pengabdian = {}
	for i in fakultas:
		pengabdian[i.fakultas_nama] = {}
		prodi = Prodi.objects.filter(fakultas=i)
		for j in prodi:
			pengabdian[i.fakultas_nama][j.prodi_nama] = len(Pengabdian.objects.filter(dosen__prodi=j).exclude(status=False))
	context = {
		'user': user,
		'statistik_pengabdian': statistik_pengabdian,
		'pengabdian': pengabdian,
	}
	return render(request, '1blood-2/index.html', context)


class PengabdianChart(APIView):
	authentication_classes = []
	permission_classes = []
	
	def get(self, request, format=None):
		labels = []
		default_items = []
		tahun = str(datetime.datetime.now().year)
		for i in range(14):
			labels.append(int(tahun) - i)
		for i in labels:
			default_items.append(len(Pengabdian.objects.filter(tahun=str(i)).exclude(status=False)))
		labels.reverse() # list tahun
		default_items.reverse() # list penelitian
		data = {
			"labels": labels,
			"default": default_items,
		}
		return Response(data)


class PengabdianProdiChart(APIView):
	authentication_classes = []
	permission_classes = []
	
	def get(self, request, format=None):
		prodi = Prodi.objects.get(prodi_nama=request.GET.get('faka'))
		labels = []
		default_items = []
		tahun = str(datetime.datetime.now().year)
		for i in range(14):
			labels.append(int(tahun) - i)
		for i in labels:
			default_items.append(len(Pengabdian.objects.filter(dosen__prodi=prodi).filter(tahun=str(i)).exclude(status=False)))
		labels.reverse() # list tahun
		default_items.reverse() # list penelitian
		data = {
			"labels": labels,
			"default": default_items,
		}
		return Response(data)


@login_required
def home(request):
	beranda = True
	user = User.objects.get(pk=request.user.pk)
	context = {
		'user': user,
		'beranda': beranda,
	}
	return render(request, '1blood-2/home.html', context)


@login_required
def penelitian_list_self(request):
	user = User.objects.get(pk=request.user.pk)
	list_penelitian_self = Penelitian.objects.filter(dosen=user.dosen.pk).order_by('-id')
	penelitian_list_self = True
	query = request.GET.get('q')
	if query:
		list_penelitian_self = list_penelitian_self.filter(
			Q(judul__icontains=query) |
			Q(tahun=query)
		).distinct()
	paginator = Paginator(list_penelitian_self, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	list_penelitian_self1 = paginator.get_page(page)
	formPenelitian = PenelitianForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if formPenelitian.is_valid():
			simpan = formPenelitian.save(commit=False)
			simpan.dosen = Dosen.objects.get(pk=user.dosen.pk)
			simpan.save()
			AnggotaPenelitian.objects.create(penelitian=simpan, level='1', nama=request.POST.get('ketua'))
			# anggota = request.POST.get('anggota')
			# d_anggota = anggota.split(',')
			# for k in d_anggota:
			# 	AnggotaPenelitian.objects.create(penelitian=simpan, level='2', nama=k.strip())
			anggota = request.POST.getlist('anggota')
			if anggota[0] != "":
				for k in anggota:
					AnggotaPenelitian.objects.create(penelitian=simpan, level='2', nama=k)
			try:
				validatori = Validatori.objects.all()
				for i in validatori:
					penerima = User.objects.get(username=i.user.username)
					notify.send(simpan, recipient=penerima, verb="Created Penelitan")
			except:
				pass
			messages.success(request, "Penelitian Berhasil Dibuat !!!")
			return redirect('lppm:penelitian_list_self')
		else:
			messages.error(request, "FAKFAK !!!")
			return redirect('lppm:penelitian_list_self')
	context = {
		'penelitian_list_self': penelitian_list_self,
		'formPenelitian': formPenelitian,
		'user': user,
		'list_penelitian_self1': list_penelitian_self1,
	}
	return render(request, '1blood-2/penelitian_self.html', context)


@login_required
def penelitian_detail_n(request, pk=None): # get list of pk_anggota
	penelitian = True
	user = User.objects.get(pk=request.user.pk)
	penelitian_detail = get_object_or_404(Penelitian, pk=pk)
	try:
		ketua = AnggotaPenelitian.objects.get(penelitian=penelitian_detail, level=1)
	except:
		ketua = None
	anggota = AnggotaPenelitian.objects.filter(penelitian=penelitian_detail, level=2)
	if request.method == 'POST':
		p = ContentType.objects.get(model='penelitian')
		aksi = request.POST.get('aksi')
		if aksi == 'update_penelitian':
			formPenelitian = PenelitianForm(request.POST or None, request.FILES or None, instance=penelitian_detail)
			if formPenelitian.is_valid():
				simpan = formPenelitian.save(commit=False)
				simpan.save()
				simpan.anggotapenelitian_set.all().delete()
				AnggotaPenelitian.objects.create(penelitian=simpan, level='1', nama=request.POST.get('ketua'))
				# anggota = request.POST.get('anggota')
				# d_anggota = anggota.split(',')
				# for k in d_anggota:
				# 	AnggotaPenelitian.objects.create(penelitian=simpan, level='2', nama=k.strip())
				anggota = request.POST.getlist('anggota')
				if anggota[0] != "":
					for k in anggota:
						AnggotaPenelitian.objects.create(penelitian=simpan, level='2', nama=k)
				try:
					validatori = Validatori.objects.all()
					for i in validatori:
						penerima = User.objects.get(username=i.user.username)
						try:
							v = penerima.notifications.get(actor_content_type=p, actor_object_id=penelitian_detail.pk, verb="Updated Penelitan {}".format(simpan.judul))
							v.delete()
						except:
							pass
						notify.send(simpan, recipient=penerima, verb="Updated Penelitan {}".format(simpan.judul))
				except:
					pass
				messages.success(request, "Edit Penelitian Sukses !!!")
				return redirect('lppm:penelitian_detail_n', pk=penelitian_detail.pk)
			else:
				messages.error(request, "Edit Penelitian ERROR !!!")
				return redirect('lppm:penelitian_detail_n', pk=penelitian_detail.pk)
		elif aksi == 'delete_penelitian':
			try:
				validatori = Validatori.objects.all()
				for i in validatori:
					dsn = User.objects.get(username=i.user.username)
					notif = dsn.notifications.filter(actor_content_type=p, actor_object_id=penelitian_detail.pk)
					for j in notif:
						j.delete()
			except:
				pass
			penelitian_detail.delete()
			messages.success(request, "Hapus Penelitian Sukses !!!")
			return redirect('lppm:penelitian_list_self')
	context = {
		'penelitian_detail': penelitian_detail,
		'anggota': anggota,
		'ketua': ketua,
		'user': user,
		'penelitian': penelitian,
	}
	return render(request, '1blood-2/p_detail1.html', context)


@login_required
def pengabdian_list_self(request):
	user = User.objects.get(pk=request.user.pk)
	list_pengabdian_self = Pengabdian.objects.filter(dosen=user.dosen.pk).order_by('-id')
	pengabdian_list_self = True
	query = request.GET.get('q')
	if query:
		list_pengabdian_self = list_pengabdian_self.filter(
			Q(judul__icontains=query) |
			Q(tahun=query)
		).distinct()
	paginator = Paginator(list_pengabdian_self, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	list_pengabdian_self1 = paginator.get_page(page)
	formPengabdian = PengabdianForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if formPengabdian.is_valid():
			simpan = formPengabdian.save(commit=False)
			simpan.dosen = Dosen.objects.get(pk=user.dosen.pk)
			simpan.save()
			AnggotaPengabdian.objects.create(pengabdian=simpan, level='1', nama=request.POST.get('ketua'))
			# anggota = request.POST.get('anggota')
			# d_anggota = anggota.split(',')
			# for k in d_anggota:
			# 	AnggotaPengabdian.objects.create(penelitian=simpan, level='2', nama=k.strip())
			anggota = request.POST.getlist('anggota')
			if anggota[0] != "":
				for k in anggota:
					AnggotaPengabdian.objects.create(pengabdian=simpan, level='2', nama=k)
			try:
				validatori = Validatori.objects.all()
				for i in validatori:
					penerima = User.objects.get(username=i.user.username)
					notify.send(simpan, recipient=penerima, verb="Created Pengabdian")
			except:
				pass
			messages.success(request, "Pengabdian Berhasil Dibuat !!!")
			return redirect('lppm:pengabdian_list_self')
		else:
			messages.error(request, "FAKFAK !!!")
			return redirect('lppm:pengabdian_list_self')
	context = {
		'pengabdian_list_self': pengabdian_list_self,
		'formPengabdian': formPengabdian,
		'list_pengabdian_self1': list_pengabdian_self1,
		'user': user,
	}
	return render(request, '1blood-2/penelitian_self.html', context)


@login_required
def pengabdian_detail_n(request, pk=None): # get list of pk_anggota
	pengabdian = True
	user = User.objects.get(pk=request.user.pk)
	pengabdian_detail = get_object_or_404(Pengabdian, pk=pk)
	try:
		ketua = AnggotaPengabdian.objects.get(pengabdian=pengabdian_detail, level=1)
	except:
		ketua = None
	anggota = AnggotaPengabdian.objects.filter(pengabdian=pengabdian_detail, level=2)
	# formPenelitian = PenelitianForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		p = ContentType.objects.get(model='pengabdian')
		aksi = request.POST.get('aksi')
		if aksi == 'update_pengabdian':
			formPengabdian = PengabdianForm(request.POST or None, request.FILES or None, instance=pengabdian_detail)
			if formPengabdian.is_valid():
				simpan = formPengabdian.save(commit=False)
				simpan.save()
				simpan.anggotapengabdian_set.all().delete()
				AnggotaPengabdian.objects.create(pengabdian=simpan, level='1', nama=request.POST.get('ketua'))
				# anggota = request.POST.get('anggota')
				# d_anggota = anggota.split(',')
				# for k in d_anggota:
				# 	AnggotaPenelitian.objects.create(penelitian=simpan, level='2', nama=k.strip())
				anggota = request.POST.getlist('anggota')
				if anggota[0] != "":
					for k in anggota:
						AnggotaPengabdian.objects.create(pengabdian=simpan, level='2', nama=k)
				try:
					validatori = Validatori.objects.all()
					for i in validatori:
						penerima = User.objects.get(username=i.user.username)
						try:
							v = penerima.notifications.get(actor_content_type=p, actor_object_id=pengabdian_detail.pk, verb="Updated Pengabdian {0}".format(simpan.judul))
							v.delete()
						except:
							pass		
						notify.send(simpan, recipient=penerima, verb="Updated Pengabdian {0}".format(simpan.judul))
				except:
					pass
				messages.success(request, "Edit Abdimas Sukses !!!")
				return redirect('lppm:pengabdian_detail_n', pk=pengabdian_detail.pk)
			else:
				messages.error(request, "Edit Abdimas ERROR !!!")
				return redirect('lppm:pengabdian_detail_n', pk=pengabdian_detail.pk)
		elif aksi == 'delete_pengabdian':
			try:
				validatori = Validatori.objects.all()
				for i in validatori:
					dsn = User.objects.get(username=i.user.username)
					notif = dsn.notifications.filter(actor_content_type=p, actor_object_id=pengabdian_detail.pk)
					for j in notif:
						j.delete()
			except:
				pass
			pengabdian_detail.delete()
			messages.success(request, "Hapus Pengabdian Sukses !!!")
			return redirect('lppm:pengabdian_list_self')
	context = {
		'pengabdian_detail': pengabdian_detail,
		'anggota': anggota,
		'ketua': ketua,
		'user': user,
		'pengabdian': pengabdian,
	}
	return render(request, '1blood-2/p_detail1.html', context)


def penelitian_list(request, nama=None):
	isi = 'penelitian'
	try:
		prodi = get_object_or_404(Prodi, prodi_nama=nama)
	except:
		prodi = ""
	penelitian_list = Penelitian.objects.filter(dosen__prodi=prodi, status=True).order_by('-id')
	query = request.GET.get('q')
	if query:
		penelitian_list = penelitian_list.filter(
			Q(judul__icontains=query) |
			Q(tahun=query)
		).distinct()
	paginator = Paginator(penelitian_list, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	penelitian_list1 = paginator.get_page(page)
	context = {
		'isi': isi,
		'prodi': prodi,
		'penelitian_list1': penelitian_list1,
	}
	return render(request, '1blood-2/penelitianProdi.html', context)


def pengabdian_list(request, nama=None):
	isi = 'pengabdian'
	try:
		prodi = get_object_or_404(Prodi, prodi_nama=nama)
	except:
		prodi = ""
	penelitian_list = Pengabdian.objects.filter(dosen__prodi=prodi, status=True).order_by('-id')
	query = request.GET.get('q')
	if query:
		penelitian_list = penelitian_list.filter(
			Q(judul__icontains=query) |
			Q(tahun=query)
		).distinct()
	paginator = Paginator(penelitian_list, 1) # Show 25 contacts per page
	page = request.GET.get('page')
	penelitian_list1 = paginator.get_page(page)
	context = {
		'isi': isi,
		'prodi': prodi,
		'penelitian_list1': penelitian_list1,
	}
	return render(request, '1blood-2/penelitianProdi.html', context)


@login_required
def validasi(request, pk=None):
	user = User.objects.get(pk=request.user.pk)
	notif_instance = user.notifications.get(pk=pk)
	notif_instance.mark_as_read()
	validasi = True
	if str(notif_instance.actor_content_type) == "penelitian":
		validasi_tipe = "Penelitian"
		validasi_instance = get_object_or_404(Penelitian, pk=notif_instance.actor.pk)
	else:
		validasi_tipe = "Pengabdian"
		validasi_instance = get_object_or_404(Pengabdian, pk=notif_instance.actor.pk)
	if request.method == "POST":
		action = request.POST.get('validation')
		if action == "good":
			validasi_instance.status = True
			validasi_instance.save()
			notify.send(validasi_instance, recipient=validasi_instance.dosen.user, verb="{0} {1} valid".format(validasi_tipe, validasi_instance.judul))
			messages.success(request, "File {} valid !!!".format(validasi_tipe))
		elif action == "bad":
			validasi_instance.status = False
			validasi_instance.save()
			notify.send(validasi_instance, recipient=validasi_instance.dosen.user, verb="{0} {1} tidak valid".format(validasi_tipe, validasi_instance.judul))
			messages.success(request, "File {} tidak valid !!!".format(validasi_tipe))
		else:
			validasi_instance.status = False
			validasi_instance.save()
			notify.send(validasi_instance, recipient=validasi_instance.dosen.user, verb="{0} {1} dibatalkan".format(validasi_tipe, validasi_instance.judul))
			messages.success(request, "Validasi file {} dibatalkan !!!".format(validasi_tipe))
		return redirect("lppm:validasi", pk=notif_instance.pk)
	context = {
		'user': user,
		'notif_instance': notif_instance,
		'validasi_instance': validasi_instance,
		'validasi_tipe': validasi_tipe,
	}
	return render(request, '1blood-2/validasi.html', context)


@login_required
def statistik(request):
	statistik = True
	try:
		user = get_object_or_404(User, pk=request.user.pk)
	except:
		user = ""
	fakultas = Fakultas.objects.all()
	penelitian = {}
	pengabdian = {}
	for i in fakultas:
		penelitian[i.fakultas_nama] = {}
		pengabdian[i.fakultas_nama] = {}
		prodi = Prodi.objects.filter(fakultas=i)
		for j in prodi:
			penelitian[i.fakultas_nama][j.prodi_nama] = len(Penelitian.objects.filter(dosen__prodi=j).exclude(status=False))
			pengabdian[i.fakultas_nama][j.prodi_nama] = len(Pengabdian.objects.filter(dosen__prodi=j).exclude(status=False))
	context = {
		'user': user,
		'statistik': statistik,
		'penelitian': penelitian,
		'pengabdian': pengabdian,

	}
	return render(request, '1blood-2/statistik.html', context)


def buat_db():
	fak = requests.get('https://api.unira.ac.id/v1/fakultas')
	fak1 = json.loads(fak.content.decode('utf-8'))
	eah = fak1['data']
	req_prodi = requests.get('https://api.unira.ac.id/v1/prodi')
	dec_req_p = json.loads(req_prodi.content.decode('utf-8'))
	list_prodi = dec_req_p['data']
	for i in eah:
		if i['id'] == 100:
			continue
		else:
			ea, created = Fakultas.objects.get_or_create(fakultas_id=i['id'], fakultas_nama=i['attributes']['nama'])
			print(ea.fakultas_id)
			print(created)
			for j in list_prodi:
				if j['relationship']['fakultas']['data']['id'] == ea.fakultas_id:
					Prodi.objects.get_or_create(fakultas=ea, prodi_id=j['id'], prodi_nama=j['attributes']['nama'])
	