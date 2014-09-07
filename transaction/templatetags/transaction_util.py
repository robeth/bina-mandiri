from django.template import Library
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers import serialize
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

register = Library()

@register.filter
def get_range( value ):
 
  return range( value )

@register.simple_tag
def nasabah_url(value):
  return "hello" + ""+ str(value)

@register.filter
def jsonify(object):
	if isinstance(object, QuerySet):
		return serialize('json', object)
	return simplejson.dumps(object)
jsonify.is_safe = True

@register.filter
def jsonify_simple(object):
	return simplejson.dumps(object)
jsonify.is_safe = True

@register.simple_tag
def pembelian_url(pembelian_id):
  return '<span class="badge badge-info" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('pembelian_detail', args=[pembelian_id]) + '", "_blank");\'' + '>B' + str(pembelian_id)+"</span>"

@register.simple_tag
def penjualan_url(penjualan_id):
  return '<span class="badge badge-success" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('penjualan_detail', args=[penjualan_id])  + '", "_blank");\'' + '>J' + str(penjualan_id)+"</span>"

@register.simple_tag
def konversi_url(konversi_id):
  return '<span class="badge badge-important" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('konversi_detail', args=[konversi_id])  + '", "_blank");\'' + '>K' + str(konversi_id)+"</span>"

@register.simple_tag
def nasabah_url(nasabah_id):
  return '<span class="badge bad" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('nasabah_detail', args=[nasabah_id])  + '", "_blank");\'' + '>N' + str(nasabah_id)+"</span>"

@register.simple_tag
def vendor_url(vendor_id):
  return '<span class="badge badge-warning" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('vendor_detail', args=[vendor_id])  + '", "_blank");\'' + '>V' + str(vendor_id)+"</span>"

@register.simple_tag
def stok_url(stok_id):
  return '<span class="badge" onmouseover="" style="cursor: pointer;" onclick=\'window.open("'+ reverse('stok_detail', args=[stok_id])  + '", "_blank");\'' + '>S' + str(stok_id)+"</span>"

@register.simple_tag
def penarikan_url(penarikan_id):
  return '<span class="badge" onmouseover="" style="cursor: pointer;"' + '>T' + str(penarikan_id)+"</span>"

@register.filter
def get_range( value ):
  return range(1, value+1)

@register.simple_tag
def calculate_gross(p):
  gross_amount = 0

  for stock in p.stocks.all():
    gross_amount += stock.jumlah * stock.harga

  return "%.2f"%gross_amount

@register.simple_tag
def calculate_bruto(p):
  bruto = 0
  for sales_stock in p.detailpenjualan_set.all():
    bruto += sales_stock.harga * sales_stock.jumlah

  return "%.2f"%bruto

@register.simple_tag
def calculate_netto(p):
  netto = 0
  for sales_stock in p.detailpenjualan_set.all():
    netto += (sales_stock.harga - sales_stock.stok.harga) * sales_stock.jumlah

  return "%.2f"%netto
# @register.simple_tag
# def calculate_netto(p):

#   netto = 0

#   for sales_stock in p.stocks.all():
#     netto += sales_stock.jumlah * sales_stock.