import factory
import datetime
from transaction.models import Nasabah

class NasabahFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Nasabah

	ktp = "TestKTP"
	nama = factory.Sequence(lambda n: "Dul Joni %02d" % n)
	alamat = "Petamburan Manggis no 7"
	telepon = "555777722"
	email = factory.Sequence(lambda n: "hello%02d@world.com" %n)
	tanggal_lahir = datetime.date.today()
	tanggal_daftar = datetime.date.today()
	jenis = "individu"