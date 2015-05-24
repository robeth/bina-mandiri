from django.conf.urls import patterns, url
from view import *


urlpatterns = patterns('',
		url(r'^$', home.index, name='home'),
		url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'transaction/login.html'}),
		url(r'^logout/$', logout.index, name='logout'),
		url(r'^nasabah/$', nasabah.index, name='nasabah'),
		url(r'^nasabah_kolektif/$', nasabah.index_kolektif, name='nasabah_kolektif'),
		url(r'^nasabah_add/$', nasabah.add, name='nasabah_add'),
		url(r'^nasabah_edit/(?P<nasabah_id>\d+)/$', nasabah.edit, name='nasabah_edit'),
		url(r'^vendor/$', vendor.index, name='vendor'),
		url(r'^vendor_add/$', vendor.add, name='vendor_add'),
		url(r'^vendor_edit/(?P<vendor_id>\d+)/$', vendor.edit, name='vendor_edit'),
		url(r'^pembelian/$', pembelian.index, name='pembelian'),
		url(r'^pembelian_add/$', pembelian.add, name='pembelian_add'),
		url(r'^penjualan/$', penjualan.index, name='penjualan'),
		url(r'^penjualan_add/$', penjualan.add, name='penjualan_add'),
		url(r'^konversi/$', konversi.index, name='konversi'),
		url(r'^konversi_add/$', konversi.add, name='konversi_add'),
		url(r'^penarikan/$', penarikan.index, name='penarikan'),
		url(r'^penarikan_add/(?P<nasabah_id>\d+)/$', penarikan.add, name='penarikan_add'),
		url(r'^kategori/$', kategori.index, name='kategori'),
		url(r'^kategori_edit/(?P<kategori_id>\d+)/$', kategori.edit, name='kategori_edit'),
		url(r'^kategori_add/$', kategori.add, name='kategori_add'),
		url(r'^nasabah_detail/(?P<nasabah_id>\d+)/$', nasabah.detail, name='nasabah_detail'),
		url(r'^vendor_detail/(?P<vendor_id>\d+)/$', vendor.detail, name='vendor_detail'),
		url(r'^pembelian_detail/(?P<pembelian_id>\d+)/$', pembelian.detail, name='pembelian_detail'),
		url(r'^pembelian_print/(?P<pembelian_id>\d+)/$', pembelian.print_version, name='pembelian_print'),
		url(r'^pembelian_del/(?P<pembelian_id>\d+)/$', pembelian.delete, name='pembelian_del'),
		url(r'^pembelian_edit/(?P<pembelian_id>\d+)/$', pembelian.edit, name='pembelian_edit'),
		url(r'^penjualan_detail/(?P<penjualan_id>\d+)/$', penjualan.detail, name='penjualan_detail'),
		url(r'^penjualan_print/(?P<penjualan_id>\d+)/$', penjualan.print_version, name='penjualan_print'),
		url(r'^penjualan_del/(?P<penjualan_id>\d+)/$', penjualan.delete, name='penjualan_del'),
		url(r'^penjualan_edit/(?P<penjualan_id>\d+)/$', penjualan.edit, name='penjualan_edit'),
		url(r'^penarikan_del/(?P<penarikan_id>\d+)/$', penarikan.delete, name='penarikan_del'),
		url(r'^konversi_detail/(?P<konversi_id>\d+)/$', konversi.detail, name='konversi_detail'),
		url(r'^konversi_del/(?P<konversi_id>\d+)/$', konversi.delete, name='konversi_del'),
		url(r'^stok_detail/(?P<stok_id>\d+)/$', report.stok_detail, name='stok_detail'),
		url(r'^penarikan_detail/(?P<penarikan_id>\d+)/$', penarikan.detail, name='penarikan_detail'),
		url(r'^penarikan_edit/(?P<penarikan_id>\d+)/$', penarikan.edit, name='penarikan_edit'),
		url(r'^laba_rugi/$', report.laba_rugi, name='laba_rugi'),
		url(r'^arus_barang/$', report.arus_barang, name='arus_barang'),
	)