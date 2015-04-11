import factory
import datetime
from transaction.models import Stok
from kategori_factory import KategoriFactory

class StokFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Stok
	kategori = factory.SubFactory(KategoriFactory)
	tanggal = datetime.date.today()
	jumlah = 10
	harga = 1025