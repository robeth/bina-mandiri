import csv
import pdb
import datetime
from transaction.models import Nasabah, Kategori, Stok, Pembelian

def run():
    filename = 'data/initial_balance.csv'
    nasabah_file = open(filename)
    reader = csv.DictReader(nasabah_file,
        fieldnames=['id', 'verbose_id', 'balance', 'jenis', 'nama'])
    kategori = Kategori.objects.get(id=1000)
    today = datetime.date.today()
    counter = 0
    for row in reader:
        print "Importing initial balance-" + str(counter)
        counter = counter + 1
        balance = float(row['balance'])
        if balance == 0: continue

        try:
            nasabah = Nasabah.objects.get(id=row['id'])
        except Nasabah.DoesNotExist:
            nasabah = Nasabah(
                id = row['id'],
                nama = row['nama'],
                jenis = row['jenis'],
                alamat = ''
            )
            nasabah.save()
            print "Create new nasabah: {0}-{1}".format(nasabah.id, nasabah.nama)

        pembelian = Pembelian(
            tanggal = today,
            nasabah = nasabah
        )
        pembelian.save()
        pembelian.stocks.create(
            kategori = kategori,
            tanggal = today,
            jumlah = 1,
            harga = balance
        )
