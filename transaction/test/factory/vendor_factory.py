import factory
import datetime
from transaction.models import Vendor

class VendorFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Vendor

	nama = factory.Sequence(lambda n: "Juragan %02d" % n)
	alamat = "Tugu Pahlawan 99"
	telepon = "999000111"
	email = (lambda n: "juragan%02d@example.com" % n)
	tanggal_daftar = datetime.date.today()