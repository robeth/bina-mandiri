import factory
import datetime
from nasabah_factory import NasabahFactory
from stok_factory import StokFactory
from transaction.models import Pembelian

class PembelianFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Pembelian

	nasabah = factory.SubFactory(NasabahFactory)
	tanggal = datetime.date.today()
	nota = "TestNota"

	@factory.post_generation
	def stocks(self, create, extracted, **kwargs):
		if not create:
			return

		if extracted:
			for stok in extracted : 
				self.stocks.add(stok)
		else:
			self.stocks.add(StokFactory())
			self.stocks.add(StokFactory())