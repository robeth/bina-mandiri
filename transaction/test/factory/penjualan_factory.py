import factory
import datetime
from vendor_factory import VendorFactory
from stok_factory import StokFactory
from transaction.models import Penjualan

class PenjualanFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Penjualan

	vendor = factory.SubFactory(VendorFactory)
	tanggal = datetime.date.today()
	nota = "TestNota"