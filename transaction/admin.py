from django.contrib import admin
from transaction.models import Nasabah, Vendor, Pembelian, Penjualan, DetailPenjualan, Stok, Kategori, Konversi, DetailIn, Penarikan

admin.site.register(Nasabah)
admin.site.register(Vendor)
admin.site.register(Pembelian)
admin.site.register(Penjualan)
admin.site.register(DetailPenjualan)
admin.site.register(Stok)
admin.site.register(Kategori)
admin.site.register(Konversi)
admin.site.register(DetailIn)
admin.site.register(Penarikan)
