from django.template import Library
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers import serialize
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
import re
from django.utils.safestring import mark_safe

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

def url_generator(url_name, url_id, prefix,label_class):
  return '<a href="%s"><span class="label %s">%s%s</span></a>' % (url_name, label_class, prefix, url_id) 

@register.simple_tag
def pembelian_url(pembelian_id):
  return url_generator(reverse('pembelian_detail', args=[pembelian_id]), pembelian_id, "B", "label-primary")

@register.simple_tag
def penjualan_url(penjualan_id):
  return url_generator(reverse('penjualan_detail', args=[penjualan_id]), penjualan_id, "J", 'label-success')

@register.simple_tag
def konversi_url(konversi_id):
  return url_generator(reverse('konversi_detail', args=[konversi_id]), konversi_id, 'K', 'label-danger')

@register.simple_tag
def nasabah_url(nasabah_id):
  return url_generator(reverse('nasabah_detail', args=[nasabah_id]), nasabah_id, 'N', 'label-info')

@register.simple_tag
def vendor_url(vendor_id):
  return url_generator(reverse('vendor_detail', args=[vendor_id]), vendor_id, 'V', 'label-warning')

@register.simple_tag
def stok_url(stok_id):
  return url_generator(reverse('stok_detail', args=[stok_id]), stok_id, 'S', 'label-default')

@register.simple_tag
def penarikan_url(penarikan_id):
  return url_generator(reverse('penarikan_detail', args=[penarikan_id]), penarikan_id, 'T', 'label-default')

@register.filter
def get_range( value ):
  return range(1, value+1)

@register.filter
def unique_item(stocks):
  res = [ s.kategori.kode for s in stocks]
  return set(res)

@register.simple_tag
def calculate_gross(p):
  gross_amount = 0

  for stock in p.stocks.all():
    gross_amount += stock.jumlah * stock.harga

  return '{0:,.2f}'.format(gross_amount)

@register.simple_tag
def calculate_total_unit_pembelian(p):
  total_unit = 0

  for stock in p.stocks.all():
    total_unit += stock.jumlah

  return '{0:,.2f}'.format(total_unit)

@register.simple_tag
def calculate_total_unit_penjualan(p):
  total_unit = 0
  for stock in p.detailpenjualan_set.all():
    total_unit += stock.jumlah
  return '{0:,.2f}'.format(total_unit)

@register.simple_tag
def calculate_bruto(p):
  bruto = 0
  for sales_stock in p.detailpenjualan_set.all():
    bruto += sales_stock.harga * sales_stock.jumlah

  return '{0:,.2f}'.format(bruto)

@register.simple_tag
def calculate_netto(p):
  netto = 0
  for sales_stock in p.detailpenjualan_set.all():
    netto += (sales_stock.harga - sales_stock.stok.harga) * sales_stock.jumlah

  return '{0:,.2f}'.format(netto)

@register.simple_tag
def calculate_konversi_value(k):
  value = 0
  for item in k.outs.all():
    value += item.harga * item.jumlah
  return '{0:,.2f}'.format(value)

@register.simple_tag
def calculate_konversi_total_input_unit(k):
  total_unit = 0
  for item in k.detailin_set.all():
    total_unit += item.jumlah
  return '{0:,.2f}'.format(total_unit)

@register.simple_tag
def calculate_konversi_total_output_unit(k):
  total_unit = 0
  for item in k.outs.all():
    total_unit += item.jumlah
  return '{0:,.2f}'.format(total_unit)

# @register.simple_tag
# def calculate_netto(p):

#   netto = 0

#   for sales_stock in p.stocks.all():
#     netto += sales_stock.jumlah * sales_stock.

@register.simple_tag
def if_empty(content):
  if not content or len(content) < 1:
    return "-"
  return content

class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')
@register.filter
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class, 
                                                    css_class, css_class), 
                                                    match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class, 
                                          string))
    else:
        return mark_safe(string.replace('>', ' class="%s">' % css_class))
    return value