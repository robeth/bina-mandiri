import csv
import datetime
from transaction.models import Pembelian, Stok, Kategori, Nasabah

saldo_dict = {}
tanggal = datetime.datetime.now().strftime("%Y-%m-%d")

# Stok.objects.all().delete()
# Pembelian.objects.all().delete()

# Create dictionary
#  {
# 	NASABAH_ID : SALDO
#  }
with open('input aug kolektif.csv', 'r') as csvfile:
  saldo_reader = csv.reader(csvfile, delimiter=';')
  for row in saldo_reader:
    saldo_dict[row[0]] = row[1]


for nasabah_id, saldo in saldo_dict.items():
  n = Nasabah.objects.get(id=nasabah_id)
  p = Pembelian(tanggal=tanggal, nasabah=n)
  p.save()
  k = Kategori.objects.get(id=1000)
  s = Stok(kategori = k,
    tanggal = '2015-08-18',
    jumlah = 1,
    harga = saldo)
  #print "N%s - Rp %s" % (nasabah_id, saldo)
  s.save()
  p.stocks.add(s)
  p.save()
