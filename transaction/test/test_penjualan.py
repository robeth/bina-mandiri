from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.transaction import atomic
from transaction.models import Penjualan, DetailPenjualan, Stok
from transaction.test.factory.nasabah_factory import *
from transaction.test.factory.kategori_factory import *
from transaction.test.factory.stok_factory import *
from transaction.test.factory.pembelian_factory import *
from transaction.test.factory.penjualan_factory import *
from transaction.test.factory.detail_penjualan_factory import *
from transaction.test.factory.konversi_factory import *
from transaction.test.factory.detail_in_factory import *
import code


class PenjualanTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username = "admin",
			password = "123",
			email = "admin@example.com")
		self.client = Client()
		self.client.login(username="admin", password="123")

	def test_index_penjualan_is_empty(self):
		response = self.client.get('/trans/penjualan/', 
			follow=True)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context["penjualan"].object_list), 0)

	def test_index_penjualan_with_2_data(self):
		stok1 = StokFactory(jumlah=10, harga=1000)
		stok2 = StokFactory(jumlah=20, harga=500)
		pembelian1 = PembelianFactory(stocks=[stok1, stok2])

		penjualan1 = PenjualanFactory()
		penjualan2 = PenjualanFactory()

		item_penjualan1 = DetailPenjualanFactory(
				penjualan=penjualan1,
				stok=stok1,
				jumlah=5,
				harga=1250
			)
		item_penjualan2 = DetailPenjualanFactory(
				penjualan=penjualan2,
				stok=stok2,
				jumlah=15,
				harga=600
			)

		response = self.client.get('/trans/penjualan/', 
			follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context["penjualan"].object_list), 2)

	def test_add_penjualan_valid_one_item_one_resource(self):
		kategori1 = KategoriFactory()
		today = datetime.date.today()
		yesterday = today - datetime.timedelta(days=1)
		
		stok1 = StokFactory(jumlah=10, 
			harga=2000, 
			kategori=kategori1,
			tanggal=yesterday)
		stok2 = StokFactory(jumlah=5, 
			harga=1000, 
			kategori=kategori1,
			tanggal=today)

		pembelian1 = PembelianFactory(stocks=[stok1], tanggal=yesterday)
		pembelian2 = PembelianFactory(stocks=[stok2], tanggal=today)
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 5,
				'harga1' : 700
			}, follow=True)  
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/penjualan/")
		self.assertEqual(len(Penjualan.objects.all()), 1)

		# Should have valid penjualan details
		penjualan1 = Penjualan.objects.all()[0]
		self.assertEqual(str(penjualan1.tanggal), '2015-04-01')
		self.assertEqual(penjualan1.nota, 'test123')
		self.assertEqual(penjualan1.vendor.id, vendor1.id)

		detailPenjualanManager1 = Penjualan.objects.all()[0].detailpenjualan_set 
		self.assertEqual(len(detailPenjualanManager1.all()), 1)

		detailPenjualan1 = detailPenjualanManager1.get(stok__id=stok1.id)

		self.assertEqual(detailPenjualan1.stok.id, stok1.id)
		self.assertEqual(detailPenjualan1.harga, 700)
		self.assertEqual(detailPenjualan1.jumlah, 5)

	def test_add_penjualan_valid_one_item_two_resources(self):
		kategori1 = KategoriFactory()
		today = datetime.date.today()
		yesterday = today - datetime.timedelta(days=1)
		
		stok1 = StokFactory(jumlah=10, 
			harga=2000, 
			kategori=kategori1,
			tanggal=yesterday)
		stok2 = StokFactory(jumlah=5, 
			harga=1000, 
			kategori=kategori1,
			tanggal=today)

		pembelian1 = PembelianFactory(stocks=[stok1], tanggal=yesterday)
		pembelian2 = PembelianFactory(stocks=[stok2], tanggal=today)
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 13,
				'harga1' : 2500
			}, follow=True)  
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/penjualan/")
		self.assertEqual(len(Penjualan.objects.all()), 1)

		# Should have valid penjualan details
		penjualan1 = Penjualan.objects.all()[0]
		self.assertEqual(str(penjualan1.tanggal), '2015-04-01')
		self.assertEqual(penjualan1.nota, 'test123')
		self.assertEqual(penjualan1.vendor.id, vendor1.id)

		detailPenjualanManager1 = Penjualan.objects.all()[0].detailpenjualan_set 
		self.assertEqual(len(detailPenjualanManager1.all()), 2)
		
		detailPenjualan1 = detailPenjualanManager1.get(stok__id=stok1.id)
		detailPenjualan2 = detailPenjualanManager1.get(stok__id=stok2.id)

		self.assertEqual(detailPenjualan1.harga, 2500)
		self.assertEqual(detailPenjualan1.jumlah, 10)
		self.assertEqual(detailPenjualan2.harga, 2500)
		self.assertEqual(detailPenjualan2.jumlah, 3)

	def test_add_penjualan_valid_multiple_item_multiple_resources(self):
		kategori1 = KategoriFactory()
		kategori2 = KategoriFactory()
		today = datetime.date.today()
		yesterday = today - datetime.timedelta(days=1)
		
		stok1_1 = StokFactory(jumlah=10, 
			harga=2000, 
			kategori=kategori1,
			tanggal=yesterday)
		stok1_2 = StokFactory(jumlah=20, 
			harga=2000, 
			kategori=kategori2,
			tanggal=yesterday)
		stok2_1 = StokFactory(jumlah=5, 
			harga=1500, 
			kategori=kategori1,
			tanggal=today)
		stok2_2 = StokFactory(jumlah=10, 
			harga=2100, 
			kategori=kategori2,
			tanggal=today)

		pembelian1 = PembelianFactory(stocks=[stok1_1, stok1_2], tanggal=yesterday)
		pembelian2 = PembelianFactory(stocks=[stok2_1, stok2_2], tanggal=today)
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 2,
				'stok1' : kategori1.kode,
				'jumlah1' : 13,
				'harga1' : 2500,
				'stok2' : kategori2.kode,
				'jumlah2' : 25,
				'harga2' : 3000
			}, follow=True)  
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.redirect_chain[0][0], "http://testserver/trans/penjualan/")
		self.assertEqual(len(Penjualan.objects.all()), 1)

		# Should have valid penjualan details
		penjualan1 = Penjualan.objects.all()[0]
		self.assertEqual(str(penjualan1.tanggal), '2015-04-01')
		self.assertEqual(penjualan1.nota, 'test123')
		self.assertEqual(penjualan1.vendor.id, vendor1.id)

		detailPenjualanManager1 = Penjualan.objects.all()[0].detailpenjualan_set 
		self.assertEqual(len(detailPenjualanManager1.all()), 4)
		
		detailPenjualan1_1 = detailPenjualanManager1.get(stok__id=stok1_1.id)
		detailPenjualan1_2 = detailPenjualanManager1.get(stok__id=stok1_2.id)
		detailPenjualan2_1 = detailPenjualanManager1.get(stok__id=stok2_1.id)
		detailPenjualan2_2 = detailPenjualanManager1.get(stok__id=stok2_2.id)

		self.assertEqual(detailPenjualan1_1.harga, 2500)
		self.assertEqual(detailPenjualan1_1.jumlah, 10)
		self.assertEqual(detailPenjualan2_1.harga, 2500)
		self.assertEqual(detailPenjualan2_1.jumlah, 3)
		self.assertEqual(detailPenjualan1_2.harga, 3000)
		self.assertEqual(detailPenjualan1_2.jumlah, 20)
		self.assertEqual(detailPenjualan2_2.harga, 3000)
		self.assertEqual(detailPenjualan2_2.jumlah, 5)

	def test_add_penjualan_multiple_resources_from_konversi(self):
		pass

	def test_add_penjualan_invalid_vendor(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id + 543,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 5,
				'harga1' : 700
			}, follow=True)  
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors['vendor'],
			[u'Select a valid choice. That choice is not one of the available choices.'])
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_add_penjualan_invalid_category(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode + str(987),
				'jumlah1' : 5,
				'harga1' : 700
			}, follow=True)  
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors,
			{u'__all__' : [u'Kategori 1 Does Not Exist'] })
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_add_penjualan_invalid_stock_amount(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

	
		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 'abc',
				'harga1' : 700
			}, follow=True) 

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors[u'__all__'],
			[u'could not convert string to float: abc'])
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_add_penjualan_insufficient_stok_amount(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

		# with self.assertRaises(ValueError):
		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : '2015-04-01',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 999,
				'harga1' : 700
			}, follow=True) 

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.context['form'].errors[u'__all__'],
			[u"[u'Kategori KAT00 Insufficient. Stok:10.0']"] )
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_add_penjualan_invalid_stock_price(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

		with self.assertRaises(ValidationError):
			response = self.client.post('/trans/penjualan_add/', {
					'tanggal' : '2015-04-01',
					'nota' : 'test123',
					'vendor' : vendor1.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 5,
					'harga1' : 'abc'
				}, follow=True) 
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_add_penjualan_invalid_date(self):
		stok1 = StokFactory(jumlah=10, harga=2000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		vendor1 = VendorFactory()

		response = self.client.post('/trans/penjualan_add/', {
				'tanggal' : 'abc',
				'nota' : 'test123',
				'vendor' : vendor1.id,
				'total' : 1,
				'stok1' : stok1.kategori.kode,
				'jumlah1' : 5,
				'harga1' : 700
			}, follow=True) 
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.context['form'].errors['tanggal'],
			['Enter a valid date.'])
		self.assertEqual(len(Penjualan.objects.all()), 0)

	def test_delete_penjualan_with_mulitple_item(self):
		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(penjualan=penjualan1)
		detailPenjualan2 = DetailPenjualanFactory(penjualan=penjualan1)

		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 2)
		self.assertEqual(len(Stok.objects.all()), 2)

		response = self.client.get('/trans/penjualan_del/%s/' % penjualan1.id)

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], "http://testserver/trans/penjualan/")
		self.assertEqual(len(Penjualan.objects.all()),0)
		self.assertEqual(len(DetailPenjualan.objects.all()), 0)
		self.assertEqual(len(Stok.objects.all()), 2)

	def test_delete_penjualan_not_exist(self):
		response = self.client.get('/trans/penjualan_del/100/')

		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers["location"][1], "http://testserver/trans/penjualan/")

	def test_edit_penjualan_not_exist(self):
		response = self.client.get('/trans/penjualan_edit/100/')

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers["location"][1], "http://testserver/trans/penjualan/")
		pass

	def test_edit_penjualan_one_item(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 2000)

	def test_edit_penjualan_one_item_add_resource(self):
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000, tanggal=today)
		pembelian1 = PembelianFactory(stocks=[stok1], tanggal=today)
		stok2 = StokFactory(kategori=kategori1, jumlah=10, harga=1000, tanggal=tomorrow)
		pembelian2 = PembelianFactory(stocks=[stok2], tanggal=tomorrow)

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 10)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : kategori1.kode,
					'jumlah1' : 15,
					'harga1' : 2000
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 2)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		edittedDetailPenjualan2 = detailPenjualanManager.get(stok__id=stok2.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 10)
		self.assertEqual(edittedDetailPenjualan1.harga, 2000)
		
		self.assertEqual(edittedDetailPenjualan2.jumlah, 5)
		self.assertEqual(edittedDetailPenjualan2.harga, 2000)

	def test_edit_penjualan_one_item_remove_resource(self):
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000, tanggal=today)
		pembelian1 = PembelianFactory(stocks=[stok1], tanggal=today)
		stok2 = StokFactory(kategori=kategori1, jumlah=10, harga=1000, tanggal=tomorrow)
		pembelian2 = PembelianFactory(stocks=[stok2], tanggal=tomorrow)

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 10)
		detailPenjualan2 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok2,
			harga=1500,
			jumlah=5
			)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : kategori1.kode,
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 2000)

	def test_edit_penjualan_multiple_item(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		stok2 = StokFactory(jumlah=50, harga=500)
		pembelian2 = PembelianFactory(stocks=[stok2])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 5)
		detailPenjualan2 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok2,
			harga=750,
			jumlah=25
			)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 2,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 1750,
					'stok2' : stok2.kategori.kode,
					'jumlah2' : 35,
					'harga2' : 800
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 2)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		edittedDetailPenjualan2 = detailPenjualanManager.get(stok__id=stok2.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 1750)
		
		self.assertNotEqual(edittedDetailPenjualan2.id, detailPenjualan2.id)
		self.assertEqual(edittedDetailPenjualan2.jumlah, 35)
		self.assertEqual(edittedDetailPenjualan2.harga, 800)

	def test_edit_penjualan_multiple_items_removal(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		stok2 = StokFactory(jumlah=50, harga=500)
		pembelian2 = PembelianFactory(stocks=[stok2])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 5)
		detailPenjualan2 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok2,
			harga=750,
			jumlah=25
			)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 1750
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 1750)

	def test_edit_penjualan_multiple_items_addition(self):
		stok1 = StokFactory(jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		stok2 = StokFactory(jumlah=50, harga=500)
		pembelian2 = PembelianFactory(stocks=[stok2])
		stok3 = StokFactory(jumlah=3, harga=250500)
		pembelian3 = PembelianFactory(stocks=[stok3])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 5)
		detailPenjualan2 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok2,
			harga=750,
			jumlah=25
			)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 3,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 1750,
					'stok2' : stok2.kategori.kode,
					'jumlah2' : 30,
					'harga2' : 700,
					'stok3' : stok3.kategori.kode,
					'jumlah3' : 2,
					'harga3' : 300500
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 3)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		edittedDetailPenjualan2 = detailPenjualanManager.get(stok__id=stok2.id)
		edittedDetailPenjualan3 = detailPenjualanManager.get(stok__id=stok3.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 1750)

		self.assertNotEqual(edittedDetailPenjualan2.id, detailPenjualan2.id)
		self.assertEqual(edittedDetailPenjualan2.jumlah, 30)
		self.assertEqual(edittedDetailPenjualan2.harga, 700)

		self.assertEqual(edittedDetailPenjualan3.jumlah, 2)
		self.assertEqual(edittedDetailPenjualan3.harga, 300500)

	def test_edit_penjualan_multiple_items_substitute(self):
		stok1 = StokFactory(jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])
		stok2 = StokFactory(jumlah=50, harga=500)
		pembelian2 = PembelianFactory(stocks=[stok2])
		stok3 = StokFactory(jumlah=3, harga=250500)
		pembelian3 = PembelianFactory(stocks=[stok3])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 5)
		detailPenjualan2 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok2,
			harga=750,
			jumlah=25
			)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 2,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 1750,
					'stok2' : stok3.kategori.kode,
					'jumlah2' : 3,
					'harga2' : 300125
				}
			)
		code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 2)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		detailPenjualanManager = edittedPenjualan1.detailpenjualan_set
		edittedDetailPenjualan1 = detailPenjualanManager.get(stok__id=stok1.id)
		edittedDetailPenjualan3 = detailPenjualanManager.get(stok__id=stok3.id)
		
		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, 8)
		self.assertEqual(edittedDetailPenjualan1.harga, 1750)

		self.assertEqual(edittedDetailPenjualan3.jumlah, 3)
		self.assertEqual(edittedDetailPenjualan3.harga, 300125)

	def test_edit_penjualan_change_vendor(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		anotherVendor = VendorFactory()

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : anotherVendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : detailPenjualan1.jumlah,
					'harga1' : detailPenjualan1.harga
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, anotherVendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_change_date(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		tomorrow = datetime.date.today() + datetime.timedelta(days=1)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{	
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(tomorrow),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : detailPenjualan1.jumlah,
					'harga1' : detailPenjualan1.harga
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, tomorrow)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_change_note(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : 'test321',
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : detailPenjualan1.jumlah,
					'harga1' : detailPenjualan1.harga
				}
			)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response._headers['location'][1], 'http://testserver/trans/penjualan_detail/%s/' % penjualan1.id)
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, 'test321')

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertNotEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_vendor(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id + 98765,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors['vendor'],
			[u'Select a valid choice. That choice is not one of the available choices.'])
		
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_date(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : 'abc',
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors['tanggal'],
			[u'Enter a valid date.'])

		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_nota(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : '1122334455667788991010',
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors['nota'],
			[u'Ensure this value has at most 20 characters (it has 22).'])

		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)
		

	def test_edit_penjualan_invalid_category(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : 'abc',
					'jumlah1' : 8,
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'].errors,
			{u'__all__' : [u'Kategori 1 Does Not Exist'] })

		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_stock_amount(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 'abc',
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.context['form'].errors[u'__all__'],
			[u'could not convert string to float: abc'])
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_insufficient_amount(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 300,
					'harga1' : 2000
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.context['form'].errors[u'__all__'],
			[u"[u'Kategori KAT17 Insufficient. Stok:10.0']"] )

		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)

	def test_edit_penjualan_invalid_price(self):
		kategori1 = KategoriFactory()
		stok1 = StokFactory(kategori=kategori1, jumlah=10, harga=1000)
		pembelian1 = PembelianFactory(stocks=[stok1])

		penjualan1 = PenjualanFactory()
		detailPenjualan1 = DetailPenjualanFactory(
			penjualan=penjualan1,
			stok=stok1,
			harga=1500,
			jumlah= 9)

		response = self.client.post('/trans/penjualan_edit/%s/' % penjualan1.id,
				{
					'penjualan_id' : penjualan1.id,
					'tanggal' : str(penjualan1.tanggal),
					'nota' : penjualan1.nota,
					'vendor' : penjualan1.vendor.id,
					'total' : 1,
					'stok1' : stok1.kategori.kode,
					'jumlah1' : 5,
					'harga1' : 'abc'
				}
			)
		# code.interact(local=dict(globals(), **locals()))
		self.assertEqual(response.context['error_messages'],
			['Invalid database operation:[u"\'abc\' value must be a decimal number."]'])
		self.assertEqual(len(Penjualan.objects.all()), 1)
		self.assertEqual(len(DetailPenjualan.objects.all()), 1)

		# Same penjualan's details
		# id, tanggal, nota, vendor
		edittedPenjualan1 = Penjualan.objects.get(id=penjualan1.id)
		self.assertEqual(edittedPenjualan1.tanggal, penjualan1.tanggal)
		self.assertEqual(edittedPenjualan1.vendor.id, penjualan1.vendor.id)
		self.assertEqual(edittedPenjualan1.nota, penjualan1.nota)

		# Changed Detail Penjualan
		# New Id, jumlah, harga
		# same stok
		edittedDetailPenjualan1 = edittedPenjualan1.detailpenjualan_set.all()[0]
		self.assertEqual(edittedDetailPenjualan1.id, detailPenjualan1.id)
		self.assertEqual(edittedDetailPenjualan1.stok.id, detailPenjualan1.stok.id)
		self.assertEqual(edittedDetailPenjualan1.jumlah, detailPenjualan1.jumlah)
		self.assertEqual(edittedDetailPenjualan1.harga, detailPenjualan1.harga)