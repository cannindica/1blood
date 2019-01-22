from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'lppm'
urlpatterns = [
	path('', views.awal, name='awal'),
	# path('login/', LoginView.as_view(template_name='login.html'), name="login"),
	path('masuk/', views.login_dosen, name="masuk"),
	path('logout/', LogoutView.as_view(next_page='lppm:masuk'), name="logout"),
	path('home/', views.home, name='home'),
	path('home/penelitian_ls/', views.penelitian_list_self, name='penelitian_list_self'),
	path('home/penelitian_ls/<int:pk>/detail/', views.penelitian_detail, name='penelitian_detail'),
	path('home/pengabdian_ls/', views.pengabdian_list_self, name='pengabdian_list_self'),
	path('penelitian_statistik/', views.penelitian_statistik, name='penelitian_statistik'),
	path('chartPenelitian/', views.PenelitianChart.as_view()),
	path('pengabdian_statistik/', views.pengabdian_statistik, name='pengabdian_statistik'),
	path('chartPengabdian/', views.PengabdianChart.as_view()),
	path('penelitian/list/<str:nama>/', views.penelitian_list, name='penelitian_list'),
	path('pengabdian/list/<str:nama>/', views.pengabdian_list, name='pengabdian_list'),
	path('validasi/<int:pk>/', views.validasi, name='validasi'),
	# path('', views.home, name='home'),
]