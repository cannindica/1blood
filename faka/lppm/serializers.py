from rest_framework import serializers
from lppm.models import Fakultas, Prodi


class FakultasSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fakultas
		fields = ('fakultas_id', 'fakultas_nama')