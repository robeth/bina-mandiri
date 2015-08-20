import csv
# from transaction.models import Pembelian, Stok, Kategori



saldo_dict = {}
tanggal = '2015-06-14'


with open('test.csv', 'r') as csvfile:
  saldo_reader = csv.reader(csvfile, delimiter=',')
  for row in saldo_reader:
    saldo_dict[row[0]] = row[1]


for nasabah_id, saldo in saldo_dict.items():
  n = Nasabah.objects.get(id=nasabah_id)
  p = Pembelian(tanggal=tanggal, nasabah=n)
  p.save()
  k = Kategori.objects.get(id=1000)
  s = Stok(kategori = k,
    tanggal = '2015-06-14',
    jumlah = 1,
    harga = saldo)
  s.save()
  p.stocks.add(s)
  p.save()