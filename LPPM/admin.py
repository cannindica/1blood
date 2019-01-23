from django.contrib import admin
from .models import Fakultas, Prodi, Dosen, Penelitian, AnggotaPenelitian, Validatori


# class ProdiInline(admin.StackedInline):
# 	model = Prodi
# 	extra = 3


# class FakultasAdmin(admin.ModelAdmin):
# 	fieldsets = [
# 		(None, {'fields': ['fakultas_nama', 'fakultas_id']})
# 	]
# 	inlines = [ProdiInline]

# admin.site.register(FakultasAdmin)

admin.site.register(Fakultas)
admin.site.register(Prodi)
admin.site.register(Dosen)
admin.site.register(Penelitian)
admin.site.register(AnggotaPenelitian)
admin.site.register(Validatori)
# admin.site.register(Pengabdian)