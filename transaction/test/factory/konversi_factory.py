import factory
import datetime
from transaction.models import Konversi

class KonversiFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Konversi

	tanggal = datetime.date.today()
	kode = factory.Sequence(lambda n: "konversi%03d" % n)