import factory
import datetime
from transaction.models import DetailIn
from konversi_factory import KonversiFactory
from stok_factory import StokFactory

class DetailInFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = DetailIn

	konversi = factory.SubFactory(KonversiFactory)
	stok = factory.SubFactory(StokFactory)
	jumlah = 1