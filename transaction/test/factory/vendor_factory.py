import factory
import datetime
from transaction.models import Vendor

class VendorFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Vendor

	nama = "Juragan Kadir"
	alamat = "Tugu Pahlawan 99"
	telepon = "999000111"
	email = "juaragan@kadir.com"
	tanggal_daftar = datetime.date.today()