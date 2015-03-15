from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from transaction.models import Nasabah, Vendor, Pembelian, Penjualan, DetailPenjualan, Stok, Kategori, Konversi, DetailIn, Penarikan
from transaction.db import q_nasabah, q_vendor, q_pembelian, q_penjualan, q_konversi, q_nasabah_detail, q_vendor_detail, q_penjualan_detail, q_pembelian_detail, q_konversi_detail, q_remaining, q_get_last_stock, q_home, q_is_pembelian_clear , q_is_konversi_clear, q_laba_rugi, q_nasabah_all, q_arus_barang
from transaction.forms import NasabahForm, VendorForm, PembelianForm, PenjualanForm, KonversiForm, PenarikanForm, KategoriForm, LoginForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.dateparse import parse_date
from transaction.helper import paginate_data, customize_pages