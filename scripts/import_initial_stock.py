import csv
import pdb
import datetime
import re
from transaction.models import Nasabah, ReportKategori, Kategori, Stok, Pembelian
from django.db.models import Q

def find_report_kategori(kode):
    search_result = re.search('(\D+)\d+', kode, re.IGNORECASE)
    initial_code = search_result.group(1) if search_result else 'L'
    initial_code = initial_code.upper()
    dictionary = {
        'AL': 'Logam',
        'BT': 'Kaca',
        'PL': 'Plastik',
        'P': 'Plastik non lembar',
        'K': 'Kertas',
        'L': 'Lain-Lain'
    }
    result = dictionary[initial_code]
    return ReportKategori.objects.get(nama=result)

def run():
    filename = 'data/initial_stock.csv'
    file = open(filename)
    reader = csv.DictReader(file,
        fieldnames=['no', 'kode', 'jumlah', 'harga', 'total'])
    nasabah = Nasabah.objects.get(id=9999)
    today = datetime.date.today()
    stocks = []

    for row in reader:
        print "Import-" + row['kode']
        try:
            kategori = Kategori.objects.get(
                Q(kode=row['kode']) | Q(kode=row['kode'].upper())
            )
        except Kategori.DoesNotExist:
            code = row['kode'].upper()
            print "Creating kategori-" + code
            kategori = Kategori.objects.create(
                kode = code,
                nama = code,
                deskripsi = code,
                satuan = 'Kg',
                stabil = 0,
                fluktuatif = 0,
                report_kategori = find_report_kategori(code)
            )

        quantity = float(row['jumlah'])
        price = float(row['harga'])
        total = quantity * price
        if total == 0: continue
        stok = Stok.objects.create(
            kategori = kategori,
            tanggal = today,
            jumlah = quantity,
            harga = price
        )
        stocks.append(stok)

    pembelian = Pembelian.objects.create(
        tanggal = today,
        nasabah = nasabah
    )

    pembelian.stocks.add(*stocks)
