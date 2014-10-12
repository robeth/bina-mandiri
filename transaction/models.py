from django.db import models
import datetime


class Nasabah(models.Model):
	ktp = models.CharField(null=True, blank=True, max_length=30)
	nama = models.CharField(max_length=50)
	alamat = models.TextField()
	telepon = models.CharField(null=True, blank=True,max_length=20)
	email = models.EmailField(null=True, blank=True)
	tanggal_lahir = models.DateField(null=True, blank=True)
	tanggal_daftar = models.DateField(default=datetime.date.today)
	foto = models.ImageField(null=True, blank=True, upload_to='nasabah')
	jenis = models.CharField(max_length=20, default="individu")
	def __unicode__(self):
		return self.nama + '-' + self.ktp

class Vendor(models.Model):
	nama = models.CharField(max_length=50)
	alamat = models.TextField()
	telepon = models.CharField(null=True, blank=True, max_length=30)
	email = models.EmailField(null=True, blank=True)
	tanggal_daftar = models.DateField(default=datetime.date.today)
	foto = models.ImageField(null=True, blank=True, upload_to='vendor')
	def __unicode__(self):
		return str(self.id) + '-' + self.nama

class Kategori(models.Model):
	kode = models.CharField(max_length=5)
	nama = models.CharField(max_length=50)
	deskripsi = models.TextField()
	satuan = models.CharField(max_length=20)
	foto = models.ImageField(null=True, blank=True, upload_to='kategori')
	stabil = models.DecimalField(max_digits=15, decimal_places=2)
	fluktuatif = models.DecimalField(max_digits=15, decimal_places=2)
	def __unicode__(self):
		return self.kode + '-' + self.nama + ' (' + self.satuan + ')'

class Stok(models.Model):
	kategori = models.ForeignKey('Kategori')
	tanggal = models.DateField()
	jumlah = models.DecimalField(max_digits=8, decimal_places=2)
	harga = models.DecimalField(max_digits=15, decimal_places=2)
	def __unicode__(self):
		return self.kategori.kode + '-' + str(self.tanggal) + ' (' + str(int(self.jumlah)) + '$'+ str(int(self.harga)) +')'

class Pembelian(models.Model):
	nasabah = models.ForeignKey('Nasabah')
	stocks = models.ManyToManyField(Stok)
	tanggal = models.DateField()
	nota = models.CharField(max_length=20, null=True, blank=True)
	def __unicode__(self):
		return self.nasabah.nama + '-' + str(self.tanggal)

class Penjualan(models.Model):
	vendor = models.ForeignKey('Vendor')
	stocks = models.ManyToManyField('Stok', through='DetailPenjualan')
	tanggal = models.DateField()	
	nota = models.CharField(max_length=20, null=True, blank=True)
	def __unicode__(self):
		return self.vendor.nama + '-' + str(self.tanggal)

class DetailPenjualan(models.Model):
	penjualan = models.ForeignKey('Penjualan')
	stok = models.ForeignKey('Stok')
	jumlah = models.DecimalField(max_digits=8, decimal_places=2)
	harga = models.DecimalField(max_digits=15, decimal_places=2)


class Konversi(models.Model):
	tanggal = models.DateField()
	ins = models.ManyToManyField('Stok', through='DetailIn', related_name='stock_in_id')
	outs = models.ManyToManyField('Stok', related_name='stock_out_id')
	kode = models.CharField(max_length=20, null=True, blank=True)
	def __unicode__(self):
		return str(self.id) + '-' + str(self.tanggal)

class DetailIn(models.Model):
	konversi = models.ForeignKey('Konversi')
	stok = models.ForeignKey('Stok')
	jumlah = models.DecimalField(max_digits=8, decimal_places=2)

class Penarikan(models.Model):
	nasabah = models.ForeignKey('Nasabah')
	tanggal = models.DateField()
	total = models.DecimalField(max_digits=15, decimal_places=2)
	nota = models.CharField(max_length=20, null=True, blank=True)
