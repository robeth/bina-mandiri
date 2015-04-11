import factory
from factory.fuzzy import FuzzyInteger
from transaction.models import Kategori

class KategoriFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Kategori

	kode = factory.Sequence( lambda n: "KAT%02d" % n)
	nama = factory.Sequence( lambda n: "Kategori-%02d" % n)
	deskripsi = "This is category description"
	satuan = factory.Iterator(["kg", "lembar", "unit"])
	stabil =  FuzzyInteger(1000, 2000, 50)
	fluktuatif = factory.LazyAttribute(lambda o: o.stabil +
			FuzzyInteger(-250, 250, 50).fuzz()
		)