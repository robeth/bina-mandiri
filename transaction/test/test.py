from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.transaction import atomic
from transaction.models import Pembelian, Stok
from transaction.test.factory.nasabah_factory import *
from transaction.test.factory.kategori_factory import *
from transaction.test.factory.stok_factory import *
from transaction.test.factory.pembelian_factory import *
from transaction.test.factory.penjualan_factory import *
from transaction.test.factory.detail_penjualan_factory import *
from transaction.test.factory.konversi_factory import *
from transaction.test.factory.detail_in_factory import *
import code

class PembelianTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="admin",
			password="123",
			email="admin@example.com")
		self.client = Client()
		self.client.login(username="admin", password="123")

	def test_index_pembelian_is_empty(self):
		response = self.client.get("/trans/pembelian/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['pembelian'].object_list), 0)

	def test_index_pembelian_with_2_data(self):
		nasabah1 = NasabahFactory()
		stok1 = StokFactory()
		stok2 = StokFactory()
		pembelian1 = PembelianFactory(nasabah=nasabah1, stocks=[stok1, stok2])
		pembelian2 = PembelianFactory()

		response = self.client.get("/trans/pembelian/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['pembelian'].object_list), 2)
		# TODO: pembelian equality test on response

	def test_add_pembelian_valid_one_item(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory() 
		
		response = self.client.post("/trans/pembelian_add/", {
				'nasabah': nasabah1.id,
				'tanggal': datetime.date.today(),
				'nota' : 'Test1',
				'total' : 1,
				'stok1' : kategori1.id,
				'jumlah1' : 2,
				'harga1' : 1000
			}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")
		# TODO: pembelian equality test on response

	def test_add_pembelian_valid_2_items(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory() 
		kategori2 = KategoriFactory()	
		
		response = self.client.post("/trans/pembelian_add/", {
				'nasabah': nasabah1.id,
				'tanggal': datetime.date.today(),
				'nota' : 'Test1',
				'total' : 2,
				'stok1' : kategori1.id,
				'jumlah1' : 2,
				'harga1' : 1000,
				'stok2' : kategori2.id,
				'jumlah2' : 3,
				'harga2' : 1000
			}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(len(Pembelian.objects.all()[0].stocks.all()), 2)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")
		# TODO: pembelian equality test on response

	def test_add_pembelian_invalid_nasabah(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory() 
		
		response = self.client.post("/trans/pembelian_add/", {
				'nasabah': nasabah1.id + 1000,
				'tanggal': datetime.date.today(),
				'nota' : 'Test1',
				'total' : 1,
				'stok1' : kategori1.id,
				'jumlah1' : 2,
				'harga1' : 1000
			}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 0)
		self.assertEqual(response.context['form'].errors, 
					{'nasabah': [u'Select a valid choice. That choice is not one of the available choices.']}
				)		

	def test_add_pembelian_invalid_kategori(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory() 
		
		response = self.client.post("/trans/pembelian_add/", {
				'nasabah': nasabah1.id,
				'tanggal': datetime.date.today(),
				'nota' : 'Test1',
				'total' : 1,
				'stok1' : kategori1.id + 100,
				'jumlah1' : 2,
				'harga1' : 1000
			}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 0)
		self.assertEqual(response.context['form'].errors, 
					{u'__all__': [u'Kategori 1 Does Not Exist']}
				)

	def test_add_pembelian_invalid_jumlah(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory()

		with self.assertRaises(ValidationError) as validation_error:
			with atomic():
				response = self.client.post('/trans/pembelian_add/', {
						'nasabah': nasabah1.id,
						'tanggal': datetime.date.today(),
						'nota' : 'Test1',
						'total' : 1,
						'stok1' : kategori1.id,
						'jumlah1' : 'abc',
						'harga1' : 1
					}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 0)

	def test_add_pembelian_invalid_harga(self):
		nasabah1 = NasabahFactory()
		kategori1 = KategoriFactory()

		with self.assertRaises(ValidationError) as validation_error:
			with atomic():
				response = self.client.post('/trans/pembelian_add/', {
						'nasabah': nasabah1.id,
						'tanggal': datetime.date.today(),
						'nota' : 'Test1',
						'total' : 1,
						'stok1' : kategori1.id,
						'jumlah1' : 1,
						'harga1' : 'abc'
					}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Pembelian.objects.all()), 0)

	def test_delete_the_only_pembelian(self):
		pembelian1 = PembelianFactory()
		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(len(Stok.objects.all()), 2)

		response = self.client.get('/trans/pembelian_del/%s/' % pembelian1.id,
			follow=True)
		# code.interact(local=dict(globals(), **locals()))

		self.assertEqual(len(Pembelian.objects.all()), 0)
		self.assertEqual(len(Stok.objects.all()), 0)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

	def test_delete_1_pembelian(self):
		pembelian1 = PembelianFactory()
		pembelian2 = PembelianFactory()
		self.assertEqual(len(Pembelian.objects.all()), 2)
		self.assertEqual(len(Stok.objects.all()), 4)

		response = self.client.get('/trans/pembelian_del/%s/' % pembelian1.id,
			follow=True)
		# code.interact(local=dict(globals(), **locals()))

		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

	def test_delete_not_exist_pembelian(self):
		response = self.client.get('/trans/pembelian_del/191919/',
			follow=True)
		# code.interact(local=dict(globals(), **locals()))

		self.assertEqual(len(Pembelian.objects.all()), 0)
		self.assertEqual(len(Stok.objects.all()), 0)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

	def test_cannot_delete_pembelian_in_penjualan(self):
		stok1 = StokFactory(jumlah=1, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detail_penjualan1 = DetailPenjualanFactory(penjualan=penjualan1, stok=stok1,
			jumlah=0.5,
			harga=1000)
		
		response = self.client.get('/trans/pembelian_del/%s/' % pembelian1.id,
			follow=True)
		# code.interact(local=dict(globals(), **locals()))

		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

	def test_cannot_delete_pembelian_in_kategori(self):
		stok1 = StokFactory(jumlah=1, harga=1000)
		stok2 = StokFactory(jumlah=2, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		konversi1 = KonversiFactory()
		konversi1.outs.add(stok2)
		detail_in1 = DetailInFactory(konversi=konversi1, stok=stok1, jumlah=0.7)
		
		response = self.client.get('/trans/pembelian_del/%s/' % pembelian1.id,
			follow=True)
		# code.interact(local=dict(globals(), **locals()))
		
		self.assertEqual(len(Pembelian.objects.all()), 1)
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

	def test_edit_pembelian_should_give_pembelian_details(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		response = self.client.get("/trans/pembelian_edit/%s/" % pembelian1.id)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['pembelian']["id"], pembelian1.id)
		self.assertEqual(response.context['pembelian']["tanggal"], str(pembelian1.tanggal))
		self.assertEqual(response.context['pembelian']["nota"], pembelian1.nota)
		self.assertEqual(response.context['pembelian']["nasabah_id"], pembelian1.nasabah.id)
		self.assertEqual(response.context['pembelian']["stocks"][0]["id"], pembelian1.stocks.all()[0].id)
		self.assertEqual(response.context['pembelian']["stocks"][0]["kategori_id"], pembelian1.stocks.all()[0].kategori.id)
		self.assertEqual(response.context['pembelian']["stocks"][0]["harga"], pembelian1.stocks.all()[0].harga)
		self.assertEqual(response.context['pembelian']["stocks"][0]["jumlah"], pembelian1.stocks.all()[0].jumlah)
		self.assertEqual(response.context['pembelian']["stocks"][0]["tanggal"], str(pembelian1.stocks.all()[0].tanggal))

	def test_edit_pembelian_redirect_to_home_on_not_exist_id(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		response = self.client.get("/trans/pembelian_edit/%s/" % (pembelian1.id + 111))
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], "http://testserver/trans/pembelian/")

	def test_edit_pembelian_same_items(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 2,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 1,
				'harga1' : 100,
				'stok2' : stok2.kategori.id,
				'jumlah2' : 2,
				'harga2' : 200
			}, follow=True)


		# code.interact(local=dict(globals(), **locals()))
		# self.assertEqual(response.status_code, 200)
		# self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian_detail/%s/" % pembelian)
		self.assertEqual(len(Pembelian.objects.all()), 1)

		# All pembelian info should be the same (including id)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# Same stock variety
		# different: id, amount, and price
		# same pembelian.tanggal
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]
		editted_stok2 = kategori2.stok_set.all()[0]

		self.assertEqual(editted_stok1.jumlah, 1)
		self.assertEqual(int(editted_stok1.harga), 100)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

		self.assertEqual(editted_stok2.jumlah, 2)
		self.assertEqual(int(editted_stok2.harga), 200)
		self.assertEqual(editted_stok2.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_change_general_info(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		nasabah1 = NasabahFactory()
		nasabah2 = NasabahFactory()
		pembelian1 = PembelianFactory(nasabah=nasabah1, stocks=[stok1, stok2])

		new_tanggal = datetime.date.today() + datetime.timedelta(days=-1)
		new_nota = "1122"

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': nasabah2.id,
				'tanggal': new_tanggal,
				'nota' : new_nota,
				'total' : 2,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 10,
				'harga1' : 1000,
				'stok2' : stok2.kategori.id,
				'jumlah2' : 20,
				'harga2' : 1500
			}, follow=True)
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian_detail/%s/" % pembelian1.id)
		self.assertEqual(len(Pembelian.objects.all()), 1)

		# Should have new info, but the same id
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(nasabah2.id, editted_pembelian.nasabah.id)
		self.assertEqual(new_tanggal, editted_pembelian.tanggal)
		self.assertEqual(new_nota, editted_pembelian.nota)

		# All stocks are the same with DIFFERENT id
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]
		editted_stok2 = kategori2.stok_set.all()[0]

		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, new_tanggal)

		self.assertEqual(editted_stok2.jumlah, 20)
		self.assertEqual(int(editted_stok2.harga), 1500)
		self.assertEqual(editted_stok2.tanggal, new_tanggal)

	def test_edit_pembelian_minus_item(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 10,
				'harga1' : 1000
			}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian_detail/%s/" % pembelian1.id)
		self.assertEqual(len(Pembelian.objects.all()), 1)

		# All pembelian info should be the same (including id)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# One stock remains. same details but different id
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 0)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_plus_item(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")
		kategori3 = KategoriFactory(kode="botol")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 3,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 10,
				'harga1' : 1000,
				'stok2' : stok2.kategori.id,
				'jumlah2' : 20,
				'harga2' : 1500,
				'stok3' : kategori3.id,
				'jumlah3' : 30,
				'harga3' : 3000
			}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian_detail/%s/" % pembelian1.id)
		self.assertEqual(len(Pembelian.objects.all()), 1)

		# All pembelian info should be the same (including id)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# Same old stocks (different id) + 1 new stok
		# same pembelian.tanggal
		self.assertEqual(len(Stok.objects.all()), 3)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 1)
		self.assertEqual(len(kategori3.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]
		editted_stok2 = kategori2.stok_set.all()[0]
		editted_stok3 = kategori3.stok_set.all()[0]

		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

		self.assertEqual(editted_stok2.jumlah, 20)
		self.assertEqual(int(editted_stok2.harga), 1500)
		self.assertEqual(editted_stok2.tanggal, pembelian1.tanggal)

		self.assertEqual(editted_stok3.jumlah, 30)
		self.assertEqual(int(editted_stok3.harga), 3000)
		self.assertEqual(editted_stok3.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_minus_previous_item_and_plus_new_item(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")
		kategori3 = KategoriFactory(kode="botol")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 2,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 10,
				'harga1' : 1000,
				'stok2' : kategori3.id,
				'jumlah2' : 30,
				'harga2' : 3000
			}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian_detail/%s/" % pembelian1.id)
		self.assertEqual(len(Pembelian.objects.all()), 1)

		# All pembelian info should be the same (including id)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks with different id
		# same pembelian.tanggal
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 0)
		self.assertEqual(len(kategori3.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]
		editted_stok3 = kategori3.stok_set.all()[0]

		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

		self.assertEqual(editted_stok3.jumlah, 30)
		self.assertEqual(int(editted_stok3.harga), 3000)
		self.assertEqual(editted_stok3.tanggal, pembelian1.tanggal)

	def test_cannot_edit_pembelian_not_exist_pembelian(self):
		kategori1 = KategoriFactory(kode="kar")
		kategori2 = KategoriFactory(kode="goni")

		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory(jumlah=20, harga=1500, kategori=kategori2)

		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		response = self.client.post("/trans/pembelian_edit/%s/" % (pembelian1.id + 100), {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 2,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 10,
				'harga1' : 1000,
				'stok2' : kategori2.id,
				'jumlah2' : 20,
				'harga2' : 1500
			}, follow=True)

		self.assertEqual(len(Pembelian.objects.all()), 1)
		# code.interact(local=dict(globals(), **locals()))
		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/pembelian/")

		# Existing pembelian should still the same
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(len(kategori1.stok_set.all()), 1)
		self.assertEqual(len(kategori2.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]
		editted_stok2 = kategori2.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

		self.assertEqual(stok2.id, editted_stok2.id)
		self.assertEqual(editted_stok2.jumlah, 20)
		self.assertEqual(int(editted_stok2.harga), 1500)
		self.assertEqual(editted_stok2.tanggal, pembelian1.tanggal)

	def test_cannot_edit_processed_pembelian_in_konversi(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		stok2 = StokFactory()
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		konversi1 = KonversiFactory()
		konversi1.outs.add(stok2)
		detail_in1 = DetailInFactory(konversi=konversi1, stok=stok1, jumlah=0.7)
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)
		# code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Some data still depend on this pembelian", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 2)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_cannot_edit_processed_pembelian_in_penjualan(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		penjualan1 = PenjualanFactory()
		detail_penjualan1 = DetailPenjualanFactory(penjualan=penjualan1, stok=stok1,
			jumlah=0.5,
			harga=1000)
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)
		# code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Some data still depend on this pembelian", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_should_handle_invalid_tanggal(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': "aaa",
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)
		# code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid form submission", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_should_handle_invalid_nota(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		penjualan1 = PenjualanFactory()
		detail_penjualan1 = DetailPenjualanFactory(penjualan=penjualan1, stok=stok1,
			jumlah=0.5,
			harga=1000)
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : "123456789123456789123456789",
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)
		# code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid form submission", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_should_handle_invalid_nasabah(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		penjualan1 = PenjualanFactory()
		detail_penjualan1 = DetailPenjualanFactory(penjualan=penjualan1, stok=stok1,
			jumlah=0.5,
			harga=1000)
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id + 1000,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)

		#code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid form submission", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)
		pass

	def test_edit_pembelian_should_handle_not_exist_stok(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
		
		penjualan1 = PenjualanFactory()
		detail_penjualan1 = DetailPenjualanFactory(penjualan=penjualan1, stok=stok1,
			jumlah=0.5,
			harga=1000)
		
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id + 100,
				'jumlah1' : 5,
				'harga1' : 500,
			}, follow=True)
		# code.interact(local=dict(globals(), **locals()))

		# Should raise exception (or simply redirected)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid form submission", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_should_handle_invalid_harga(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])

		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : 5,
				'harga1' : "aaa",
			}, follow=True)
		
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid database operation", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)

	def test_edit_pembelian_should_handle_invalid_jumlah(self):
		kategori1 = KategoriFactory(kode="kar")
		stok1 = StokFactory(jumlah=10, harga=1000, kategori=kategori1)
		pembelian1 = PembelianFactory(stocks=[stok1])
			
		response = self.client.post("/trans/pembelian_edit/%s/" % pembelian1.id, {
				'nasabah': pembelian1.nasabah.id,
				'tanggal': pembelian1.tanggal,
				'nota' : pembelian1.nota,
				'total' : 1,
				'stok1' : stok1.kategori.id,
				'jumlah1' : "aaa",
				'harga1' : 500,
			}, follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.redirect_chain), 0)
		self.assertIn("Invalid database operation", response.context['error_messages'])

		# Existing pembelian should still the same
		self.assertEqual(len(Pembelian.objects.all()), 1)
		editted_pembelian = Pembelian.objects.all()[0]
		self.assertEqual(pembelian1.id, editted_pembelian.id)
		self.assertEqual(pembelian1.nasabah.id, editted_pembelian.nasabah.id)
		self.assertEqual(pembelian1.tanggal, editted_pembelian.tanggal)
		self.assertEqual(pembelian1.nota, editted_pembelian.nota)

		# All stocks should be the unchanged (including id)
		self.assertEqual(len(Stok.objects.all()), 1)
		self.assertEqual(len(kategori1.stok_set.all()), 1)

		editted_stok1 = kategori1.stok_set.all()[0]

		self.assertEqual(stok1.id, editted_stok1.id)
		self.assertEqual(editted_stok1.jumlah, 10)
		self.assertEqual(int(editted_stok1.harga), 1000)
		self.assertEqual(editted_stok1.tanggal, pembelian1.tanggal)