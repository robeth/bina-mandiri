import factory
import datetime
from transaction.models import DetailPenjualan
from penjualan_factory import PenjualanFactory
from stok_factory import StokFactory

class DetailPenjualanFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = DetailPenjualan

	penjualan = factory.SubFactory(PenjualanFactory)
	stok = factory.SubFactory(StokFactory)
	jumlah = 1
	harga = 1000