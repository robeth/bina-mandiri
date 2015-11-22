from django.db import connection
from transaction.models import Stok, Pembelian, Konversi, Penjualan, Nasabah
from datetime import datetime
def to_dict(c):
	return [ dict(zip([col[0] for col in c.description], row)) for row in c.fetchall()]

def strip(query):
	return query.replace('\n', ' ').replace('\t', ' ')

def q_nasabah(kind):
	c = connection.cursor()
	c.execute(strip(
		"""SELECT n.id,
		       n.nama,
		       n.alamat,
		       n.telepon,
			   n.nama_pj,
			   n.no_induk,
		       coalesce(inning.total,0) AS 'In',
		       coalesce(outting.total,0) AS 'Out'
		FROM transaction_nasabah n
		LEFT OUTER JOIN
		 (SELECT p.nasabah_id AS id,
		         sum(s.jumlah*s.harga) AS total
		  FROM transaction_pembelian p
		  JOIN transaction_pembelian_stocks ps ON p.id = ps.pembelian_id
		  JOIN transaction_stok s ON s.id = ps.stok_id
		  GROUP BY p.nasabah_id) AS inning ON n.id = inning.id
		LEFT OUTER JOIN
		 (SELECT n.id AS id,
		         sum(p.total) AS total
		  FROM transaction_nasabah n
		  JOIN transaction_penarikan p ON n.id = p.nasabah_id
		  GROUP BY n.id) AS outting ON n.id = outting.id
		WHERE n.jenis=%s
		"""), [kind])
	res = to_dict(c)
	for t in res:
		t['saldo'] = t['In'] - t['Out']
	return res

def q_nasabah_all():
	c = connection.cursor()
	c.execute("select n.id, n.nama, n.alamat, n.telepon, coalesce(inning.total,0) as 'In', coalesce(outting.total,0) as 'Out' from transaction_nasabah n left outer join (select p.nasabah_id as id, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on s.id = ps.stok_id group by p.nasabah_id) as inning on n.id = inning.id left outer join (select n.id as id, sum(p.total) as total from transaction_nasabah n join transaction_penarikan p on n.id = p.nasabah_id group by n.id) as outting on n.id = outting.id")
	res = to_dict(c)
	for t in res:
		t['saldo'] = t['In'] - t['Out']
	return res

def q_vendor():
	c = connection.cursor()
	c.execute(strip(
		"""SELECT v.id,
		       v.nama,
		       v.alamat,
		       v.telepon,
		       coalesce(r.sid,-1) AS stokid,
		       r.kode,
		       r.nama AS stok_nama,
		       r.deskripsi,
		       v.nama,
		       v.alamat,
		       v.telepon,
		       coalesce(r.gross,0) AS bruto,
		       coalesce(r.netto,0) AS netto
		FROM transaction_vendor v
		LEFT OUTER JOIN
		 (SELECT p.vendor_id AS id,
		         s.id AS sid,
		         s.kode,
		         s.nama,
		         s.deskripsi,
		         sum(dp.jumlah*dp.harga) AS gross,
		         sum(dp.jumlah*(dp.harga-s.harga)) AS netto
		  FROM transaction_detailpenjualan dp
		  JOIN transaction_penjualan p ON dp.penjualan_id = p.id
		  JOIN transaction_stok_det s ON s.id = dp.stok_id
		  GROUP BY p.vendor_id,
		           s.id) AS r ON v.id = r.id
		ORDER BY v.id ASC,
		         bruto DESC
		 """))
	res = to_dict(c)

	res2 = {}

	for t in res:
		if t['id'] in res2:
			res2[t['id']]['sum_bruto'] = res2[t['id']]['sum_bruto'] + t['bruto']
			res2[t['id']]['sum_netto'] = res2[t['id']]['sum_netto'] + t['netto']
			if t['kode'] in res2[t['id']]['kategori']:
				res2[t['id']]['kategori'][t['kode']]['nilai'] += t['bruto']
			else:
				res2[t['id']]['kategori'][t['kode']] = {'nama':t['stok_nama'], 'nilai':t['bruto']}
		else:
			res2[t['id']] = t
			t['sum_bruto'] = t['bruto']
			t['sum_netto'] = t['netto']
			t['kategori'] = { t['kode'] : {'nama':t['stok_nama'], 'nilai':t['bruto']}}
	return res2

def q_pembelian(limit=-1):
	c = connection.cursor()
	if limit > 0:
		c.execute("select p.id, p.nota, r.sid, r.kode, r.nama as snama, n.nama as vnama, r.tanggal, r.jumlah, r.harga, r.harga*r.jumlah as total from transaction_pembelian p left outer join (  select ps.pembelian_id as id, s.id as sid, s.kode, s.nama, s.tanggal, s.jumlah, s.harga  from transaction_pembelian_stocks ps join  (   select s.id, k.kode, k.nama, s.tanggal, s.jumlah, s.harga   from transaction_kategori k join transaction_stok s on k.id = s.kategori_id  ) s on  ps.stok_id=s.id ) r on p.id = r.id join transaction_nasabah n on n.id = p.nasabah_id order by r.tanggal desc LIMIT %s", [limit])
	else:
		c.execute("select p.id, p.nota, r.sid, r.kode, r.nama as snama, n.nama as vnama, r.tanggal, r.jumlah, r.harga, r.harga*r.jumlah as total from transaction_pembelian p left outer join (  select ps.pembelian_id as id, s.id as sid, s.kode, s.nama, s.tanggal, s.jumlah, s.harga  from transaction_pembelian_stocks ps join  (   select s.id, k.kode, k.nama, s.tanggal, s.jumlah, s.harga   from transaction_kategori k join transaction_stok s on k.id = s.kategori_id  ) s on  ps.stok_id=s.id ) r on p.id = r.id join transaction_nasabah n on n.id = p.nasabah_id order by r.tanggal desc")
	res = to_dict(c)

	res2 = {}

	for t in res:
		if t['id'] in res2:
			res2[t['id']]['sum'] += t['total']
			if t['kode'] in res2[t['id']]['kategori']:
				res2[t['id']]['kategori'][t['kode']]['nilai'] += t['total']
			else:
				res2[t['id']]['kategori'][t['kode']] = {'nama':t['snama'], 'nilai':t['total']}
		else:
			res2[t['id']] = t
			t['sum'] = t['total']
			t['kategori'] = { t['kode'] : {'nama':t['snama'], 'nilai':t['total']}}
	return res2

def q_penjualan(vendor_id=None, limit=-1):
	c = connection.cursor()
	if vendor_id==None:
		if limit > 0:
			c.execute("select p.id, p.nota, p.vendor_id, v.nama as vnama, s.id as sid, s.nama as snama, s.kode as kode, s.deskripsi as ket, p.tanggal, sum(dp.jumlah*dp.harga) as bruto, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp right outer join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id join transaction_vendor v on p.vendor_id=v.id group by p.id, s.id order by p.tanggal desc, bruto desc LIMIT %s", [limit])
		else:
			c.execute("select p.id, p.nota, p.vendor_id, v.nama as vnama, s.id as sid, s.nama as snama, s.kode as kode, s.deskripsi as ket, p.tanggal, sum(dp.jumlah*dp.harga) as bruto, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp right outer join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id join transaction_vendor v on p.vendor_id=v.id group by p.id, s.id order by p.tanggal desc, bruto desc")
	else :
		c.execute("select p.id, p.nota, p.vendor_id, v.nama as vnama, s.id as sid, s.nama as snama, s.kode as kode, s.deskripsi as ket, p.tanggal, sum(dp.jumlah*dp.harga) as bruto, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp right outer join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id join transaction_vendor v on p.vendor_id=v.id where v.id = %s group by p.id, s.id order by p.tanggal desc, bruto desc", [vendor_id])
	res = to_dict(c)
	res2 = {}

	for t in res:
		if t['id'] in res2:
			res2[t['id']]['sum_bruto'] = res2[t['id']]['sum_bruto'] + t['bruto']
			res2[t['id']]['sum_netto'] = res2[t['id']]['sum_netto'] + t['netto']
			if t['kode'] in res2[t['id']]['kategori']:
				res2[t['id']]['kategori'][t['kode']]['nilai'] += t['bruto']
			else:
				res2[t['id']]['kategori'][t['kode']] = {'nama':t['snama'], 'nilai':t['bruto']}
		else:
			res2[t['id']] = t
			t['sum_bruto'] = t['bruto']
			t['sum_netto'] = t['netto']
			t['kategori'] = { t['kode'] : {'nama':t['snama'], 'nilai':t['bruto']}}
	return res2

def q_konversi(limit=-1):
	c = connection.cursor()
	if limit > 0:
		c.execute("select * from ( (select 1 as is_out, k.id, k.tanggal, k.kode as kodenota, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, sd.jumlah as jumlah2 from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id) UNION (select 0 as is_out, k.id, k.tanggal, k.kode as kodenota, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, di.jumlah as jumlah2 from transaction_konversi k join transaction_detailin di on k.id = di.konversi_id join transaction_stok_det sd on di.stok_id = sd.id)) a order by a.id, is_out LIMIT %s", [limit])
	else:
		c.execute("select * from ( (select 1 as is_out, k.id, k.tanggal, k.kode as kodenota, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, sd.jumlah as jumlah2 from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id) UNION (select 0 as is_out, k.id, k.tanggal, k.kode as kodenota, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, di.jumlah as jumlah2 from transaction_konversi k join transaction_detailin di on k.id = di.konversi_id join transaction_stok_det sd on di.stok_id = sd.id)) a order by a.id, is_out")

	res = to_dict(c)

	res2 = {}
	for t in res:
		if t['id'] in res2:
			if t['is_out'] == 1:
				res2[t['id']]['total_out'] += t['harga']*t['jumlah']
				res2[t['id']]['out'][t['stok_id']]= {'kode':t['kode'],'nama':t['nama'], 'tanggal': t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga']}
			else:
				res2[t['id']]['total_in'] += t['jumlah2'] * t['harga']
				res2[t['id']]['in'][t['stok_id']]= {'kode':t['kode'],'nama':t['nama'], 'tanggal': t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'jumlah2':t['jumlah2']}
		else:
			res2[t['id']] = t
			t['in'] = {}
			t['out'] = {}
			t['total_in'] = 0
			t['total_out'] = 0
			if t['is_out'] == 1:
				t['total_out'] = t['harga']*t['jumlah']
				t['out'][t['stok_id']]= {'kode':t['kode'], 'nama':t['nama'], 'tanggal': t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'nilai': t['harga']*t['jumlah'] }
			else:
				t['total_in'] = t['jumlah2'] * t['harga']
				t['in'][t['stok_id']]= {'kode':t['kode'], 'nama':t['nama'], 'tanggal':t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'jumlah2':t['jumlah2'], 'nilai': t['harga']*t['jumlah']}
	return res2

def q_konversi2(konversi_id):
	c = connection.cursor()
	c.execute("select * from ( (select 1 as is_out, k.id, k.tanggal, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, sd.jumlah as jumlah2 from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id where k.id=%s) UNION (select 0 as is_out, k.id, k.tanggal, sd.tanggal as stanggal, sd.id as stok_id, sd.kode, sd.nama, sd.deskripsi, sd.jumlah, sd.harga, di.jumlah as jumlah2 from transaction_konversi k join transaction_detailin di on k.id = di.konversi_id join transaction_stok_det sd on di.stok_id = sd.id where k.id=%s)) a order by a.id, is_out", [konversi_id, konversi_id])

	res = to_dict(c)

	res2 = {}
	for t in res:
		if t['id'] in res2:
			if t['is_out'] == 1:
				res2[t['id']]['total_out'] += t['harga']*t['jumlah']
				res2[t['id']]['total_unit_out'] += t['jumlah']
				res2[t['id']]['out'].append({'id':t['stok_id'], 'kode':t['kode'], 'nama':t['nama'], 'tanggal': t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'nilai': t['harga']*t['jumlah'] })
			else:
				res2[t['id']]['total_in'] += t['jumlah2'] * t['harga']
				res2[t['id']]['total_unit_in'] += t['jumlah2']
				res2[t['id']]['in'].append({'id':t['stok_id'], 'kode':t['kode'], 'nama':t['nama'], 'tanggal':t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'jumlah2':t['jumlah2'], 'nilai': t['harga']*t['jumlah']})
		else:
			res2[t['id']] = t
			t['in'] = []
			t['out'] = []
			t['total_in'] = 0
			t['total_out'] = 0
			t['total_unit_in'] = 0
			t['total_unit_out'] = 0
			if t['is_out'] == 1:
				t['total_out'] = t['harga']*t['jumlah']
				t['total_unit_out'] = t['jumlah']
				t['out'].append({'id':t['stok_id'], 'kode':t['kode'], 'nama':t['nama'], 'tanggal': t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'nilai': t['harga']*t['jumlah'] })
			else:
				t['total_in'] = t['jumlah2'] * t['harga']
				t['total_unit_in'] = t['jumlah2']
				t['in'].append({'id':t['stok_id'], 'kode':t['kode'], 'nama':t['nama'], 'tanggal':t['stanggal'], 'jumlah':t['jumlah'], 'harga':t['harga'], 'jumlah2':t['jumlah2'], 'nilai': t['harga']*t['jumlah2']})
	return res2

def q_nasabah_detail(nasabah_id):
	res = {}

	c = connection.cursor()
	c.execute(strip(
		"""SELECT n.id,
			       n.jenis,
			       n.ktp,
			       n.nama,
			       n.alamat,
			       n.telepon,
			       n.tanggal_daftar,
			       n.tanggal_lahir,
			       n.foto,
				   n.nama_pj,
				   n.no_induk,
			       coalesce(inning.total,0) AS 'In',
			       coalesce(outting.total,0) AS 'Out'
			FROM transaction_nasabah n
			LEFT OUTER JOIN
			 (SELECT p.nasabah_id AS id,
			         sum(s.jumlah*s.harga) AS total
			  FROM transaction_pembelian p
			  JOIN transaction_pembelian_stocks ps ON p.id = ps.pembelian_id
			  JOIN transaction_stok s ON s.id = ps.stok_id
			  GROUP BY p.nasabah_id) AS inning ON n.id = inning.id
			LEFT OUTER JOIN
			 (SELECT n.id AS id,
			         sum(p.total) AS total
			  FROM transaction_nasabah n
			  JOIN transaction_penarikan p ON n.id = p.nasabah_id
			  GROUP BY n.id) AS outting ON n.id = outting.id
			WHERE n.id=%s"""),[nasabah_id])
	temp = to_dict(c)
	res['general'] = None
	if len(temp) > 0:
		res['general'] = temp[0]
		temp[0]['saldo'] = temp[0]['In'] - temp[0]['Out']

	c.execute("select p.id, r.sid, r.kode, r.nama as snama, n.nama as vnama, r.tanggal, r.jumlah, r.harga, r.harga*r.jumlah as total from transaction_pembelian p left outer join (  select ps.pembelian_id as id, s.id as sid, s.kode, s.nama, s.tanggal, s.jumlah, s.harga  from transaction_pembelian_stocks ps join  (   select s.id, k.kode, k.nama, s.tanggal, s.jumlah, s.harga   from transaction_kategori k join transaction_stok s on k.id = s.kategori_id  ) s on  ps.stok_id=s.id ) r on p.id = r.id join transaction_nasabah n on n.id = p.nasabah_id where n.id=%s order by p.id asc", [nasabah_id])
	pembelian = to_dict(c)
	res2 = {}

	for t in pembelian:
		if t['id'] in res2:
			res2[t['id']]['sum'] += t['total']
			res2[t['id']]['sum_weight'] += t['jumlah']
			if t['kode'] in res2[t['id']]['kategori']:
				res2[t['id']]['kategori'][t['kode']]['nilai'] += t['total']
			else:
				res2[t['id']]['kategori'][t['kode']] = {'nama':t['snama'], 'nilai':t['total']}
		else:
			res2[t['id']] = t
			t['sum'] = t['total']
			t['sum_weight'] = t['jumlah']
			t['kategori'] = { t['kode'] : {'nama':t['snama'], 'nilai':t['total']}}
	res['pembelian'] = res2

	c.execute("select p.* from transaction_nasabah n join transaction_penarikan p on n.id = p.nasabah_id where n.id = %s", [nasabah_id])
	res['penarikans'] = Nasabah.objects.filter(id=nasabah_id)[0].penarikan_set.all()

	c.execute("select s.kode, s.nama, sum(s.jumlah) as jumlah, sum(s.jumlah*s.harga) as nilai from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok_det s on ps.stok_id = s.id where p.nasabah_id = %s group by s.kode", [nasabah_id])
	res['stok'] = to_dict(c)

	res['safe_delete'] = Nasabah.objects.get(id=nasabah_id).is_safe_to_be_deleted()

	return res

def q_vendor_detail(vendor_id):
	res = {}
	res['penjualan'] = q_penjualan(vendor_id)
	res['total_bruto'] = 0
	res['total_netto'] = 0
	for k, v in res['penjualan'].iteritems():
		res['total_bruto'] += v['sum_bruto']
		res['total_netto'] += v['sum_netto']

	c = connection.cursor()
	c.execute("select s.kode, s.nama, s.deskripsi, sum(dp.jumlah) as jumlah, sum(dp.jumlah*dp.harga) as nilai, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id where p.vendor_id = %s group by s.kode", [vendor_id])
	res['stok'] = to_dict(c)

	return res;

def q_penjualan_detail(penjualan_id):
	res = {}
	c = connection.cursor()
	c.execute("select s.id as sid, s.nama as snama, s.kode as kode, s.tanggal as tanggal, s.harga as sharga, dp.harga as pharga, dp.jumlah as jumlah, s.jumlah as sjumlah, dp.jumlah*dp.harga as bruto, dp.jumlah*s.harga as invest, dp.jumlah*(dp.harga-s.harga) as netto from transaction_detailpenjualan dp join transaction_stok_det s on s.id = dp.stok_id where dp.penjualan_id=%s order by dp.id", [penjualan_id])
	res['penjualan_detail'] = to_dict(c)
	res['total_penjualan']=0
	res['total_pembelian']=0
	res['total_profit'] =0
	res['total_unit'] = 0
	for v in res['penjualan_detail']:
		res['total_penjualan'] += v['bruto']
		res['total_pembelian'] += v['invest']
		res['total_profit'] += v['netto']
		res['total_unit'] += v['jumlah']

	return res

def q_pembelian_detail(pembelian_id):
	res = {}
	res2 = {}

	c = connection.cursor()
	c.execute("select * from (( select if(dp.jumlah is null, 0,1) as status, s.*, s.jumlah*s.harga as nilai_beli, dp.jumlah as jumlah_keluar, dp.harga as harga_keluar, dp.jumlah*dp.harga as nilai_keluar, dp.jumlah*(dp.harga-s.harga) as netto, dp.penjualan_id as kode_status from ( select s.* from transaction_pembelian_stocks p join transaction_stok_det s on p.stok_id = s.id where p.pembelian_id = %s ) s left outer join transaction_detailpenjualan dp on s.id = dp.stok_id) Union (select if(di.jumlah is null, 0,2) as status,s.*, s.jumlah*s.harga as nilai_beli, di.jumlah as jumlah_keluar, s.harga as harga_keluar, di.jumlah*s.harga as nilai_keluar , 0 as netto, di.konversi_id as kode_status from ( select s.* from transaction_pembelian_stocks p join transaction_stok_det s on p.stok_id = s.id where p.pembelian_id = %s ) s left outer join transaction_detailin di on s.id = di.stok_id)) a order by a.id", [pembelian_id, pembelian_id])
	res['pembelian_detail'] = res2
	temp = to_dict(c)

	res['total_penjualan']=0
	res['total_pembelian']=0
	res['total_profit'] =0
	res['total_unit_pembelian']=0
	res['total_unit_penjualan']=0

	for t in temp:
		if t['id'] in res2:
			if t['status'] != 0:
				res2[t['id']]['keluaran'].append(t)
				res['total_penjualan'] += t['nilai_keluar']
				res['total_unit_penjualan'] += t['jumlah_keluar']
				res['total_profit'] += t['netto']
				res2[t['id']]['sisa'] -= t['jumlah_keluar']
		else:
			res2[t['id']] = t
			res2[t['id']]['keluaran'] = []
			res2[t['id']]['sisa'] = t['jumlah']
			res['total_pembelian'] += t['nilai_beli']
			res['total_unit_pembelian'] += t['jumlah']
			if t['status'] != 0:
				res2[t['id']]['keluaran'].append(t)
				res['total_penjualan'] += t['nilai_keluar']
				res['total_unit_penjualan'] += t['jumlah_keluar']
				res['total_profit'] += t['netto']
				res2[t['id']]['sisa'] -= t['jumlah_keluar']

	for k, v in res2.iteritems():
		v['length'] = len(v['keluaran'])
		if v['length'] < 1:
			v['has'] = False
		else:
			v['has'] = True

	return res

def q_is_pembelian_clear(pembelian_id):
	p = Pembelian.objects.filter(id=pembelian_id)
	if p:
		p = p[0]
		stocks = p.stocks.all()
		if p.detailpenarikan_set.all():
			return False
		for stock in stocks:
			if stock.penjualan_set.all() or stock.detailin_set.all():
				return False
	else:
		return False
	return True

def q_is_konversi_clear(konversi_id):
	k = Konversi.objects.filter(id=konversi_id)
	if k:
		k = k[0]
		stocks = k.outs.all()
		for stock in stocks:
			if stock.penjualan_set.all() or stock.detailin_set.all():
				return False
	else:
		return False
	return True

def q_konversi_detail(konversi_id):
	res= {}
	temp = q_konversi2(konversi_id)

	if len(temp) < 1:
		res['detail'] = {}
	else:
		res['detail'] = temp[temp.keys()[0]]
		res['length'] = max(len(res['detail']['in']), len(res['detail']['out']))

	# import ipdb
	# ipdb.set_trace()
	c = connection.cursor()
	c.execute("select * from (( select if(dp.jumlah is null, 0,1) as status, s.*, s.jumlah*s.harga as nilai_beli, dp.jumlah as jumlah_keluar, dp.harga as harga_keluar, dp.jumlah*dp.harga as nilai_keluar, dp.jumlah*(dp.harga-s.harga) as netto, dp.penjualan_id as kode_status  from ( select s.* from transaction_konversi_outs p join transaction_stok_det s on p.stok_id = s.id where p.konversi_id = %s ) s left outer join transaction_detailpenjualan dp on s.id = dp.stok_id) Union (select if(di.jumlah is null, 0,2) as status, s.*, s.jumlah*s.harga as nilai_beli, di.jumlah as jumlah_keluar, s.harga as harga_keluar, di.jumlah*s.harga as nilai_keluar, 0 as netto, di.konversi_id as kode_status  from ( select s.* from transaction_konversi_outs p join transaction_stok_det s on p.stok_id = s.id where p.konversi_id = %s ) s left outer join transaction_detailin di on s.id = di.stok_id)) a order by a.id", [konversi_id, konversi_id])
	resTracking = {}
	res['tracking'] = resTracking
	temp = to_dict(c)

	res['total_penjualan']=0
	res['total_pembelian']=0
	res['total_profit'] =0
	res['total_unit_penjualan']=0
	res['total_unit_pembelian']=0

	for t in temp:
		if t['id'] in resTracking:
			if t['status'] != 0:
				resTracking[t['id']]['keluaran'].append(t)
				res['total_penjualan'] += t['nilai_keluar']
				res['total_profit'] += t['netto']
				res['total_unit_penjualan'] += t['jumlah_keluar']
				resTracking[t['id']]['sisa'] -= t['jumlah_keluar']
		else:
			resTracking[t['id']] = t
			resTracking[t['id']]['keluaran'] = []
			resTracking[t['id']]['sisa'] = t['jumlah']
			res['total_pembelian'] += t['nilai_beli']
			res['total_unit_pembelian'] += t['jumlah']
			if t['status'] != 0:
				resTracking[t['id']]['keluaran'].append(t)
				res['total_penjualan'] += t['nilai_keluar']
				res['total_profit'] += t['netto']
				res['total_unit_penjualan'] += t['jumlah_keluar']
				resTracking[t['id']]['sisa'] -= t['jumlah_keluar']

	for k, v in resTracking.iteritems():
			v['length'] = len(v['keluaran'])
			if v['length'] < 1:
				v['has'] = False
			else:
				v['has'] = True
	return res

def q_remaining():
	c = connection.cursor()
	c.execute("select sr.kode, k.nama, k.satuan, k.stabil, sr.jumlah_in, sr.jumlah_penjualan, sr.jumlah_konversi, sr.sisa from stok_remain sr join transaction_kategori k on sr.kode = k.kode")
	res = to_dict(c)

	for r in res:
		r['sisa'] = float(r['sisa'])
		r['stabil'] = float(r['stabil'])
		r['jumlah_konversi'] = float(r['jumlah_konversi'])
		r['jumlah_in'] = float(r['jumlah_in'])
		r['jumlah_penjualan'] = float(r['jumlah_penjualan'])
	return res

def q_remaining_dict():
	temp = q_remaining()
	res = {}

	for t in temp:
		res[t['kode']] = t

	return res

def q_reclaimed_stocks(penjualan_id):
	res = {}
	detailPenjualanList = Penjualan.objects.get(id=penjualan_id).detailpenjualan_set.all()

	for detailPenjualan in detailPenjualanList:
		kodeKategori = detailPenjualan.stok.kategori.kode
		if not kodeKategori in res:
			res[kodeKategori] = 0
		res[kodeKategori] += float(detailPenjualan.jumlah)

	return res


def q_last_stock(kode):
	c = connection.cursor()
	c.execute(strip(
		"""SELECT sd.id AS id,
		       sd.tanggal,
		       sd.kode,
		       sd.jumlah AS jumlah_in,
		       coalesce(i.jumlah,0) AS jumlah_konversi,
		       coalesce(p.jumlah, 0) AS jumlah_penjualan,
		       sd.jumlah - coalesce(i.jumlah,0)- coalesce(p.jumlah,0) AS sisa
		FROM transaction_stok_det sd
		LEFT OUTER JOIN
		 ( SELECT ki.stok_id,
		          sum(ki.jumlah) as jumlah
		  FROM transaction_detailin ki
		  GROUP BY ki.stok_id ) i ON sd.id = i.stok_id
		LEFT OUTER JOIN
		 ( SELECT ss.stok_id,
		          sum(ss.jumlah) as jumlah
		  FROM transaction_detailpenjualan ss
		  GROUP BY ss.stok_id ) p ON sd.id = p.stok_id
		WHERE sd.kode = %s
		ORDER BY sd.tanggal"""), [kode])
	res = to_dict(c)

	for r in res:
		r['sisa'] = float(r['sisa'])
		r['jumlah_konversi'] = float(r['jumlah_konversi'])
		r['jumlah_in'] = float(r['jumlah_in'])
		r['jumlah_penjualan'] = float(r['jumlah_penjualan'])

	res = [ r for r in res if r['sisa'] > 0]

	return res

def q_get_last_stock(kode, jumlah):
	res = []
	temp = q_last_stock(kode)

	need = float(jumlah)
	counter = 0

	while counter < len(temp) and need > 0:
		take = min(need, temp[counter]['sisa'])
		need -= float(take)
		res.append({'id': temp[counter]['id'], 'jumlah': take})
		counter += 1

	return res

def q_nasabah_detail_only(nasabah_id):
	res = {}

	c = connection.cursor()
	c.execute("select n.id, n.ktp, n.nama, n.alamat, n.telepon, n.tanggal_daftar, n.tanggal_lahir, coalesce(inning.total,0) as 'In', coalesce(outting.total,0) as 'Out' from transaction_nasabah n left outer join (select p.nasabah_id as id, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on s.id = ps.stok_id group by p.nasabah_id) as inning on n.id = inning.id left outer join (select n.id as id, sum(p.total) as total from transaction_nasabah n join transaction_penarikan p on n.id = p.nasabah_id group by n.id) as outting on n.id = outting.id where n.id=%s",[nasabah_id])
	temp = to_dict(c)
	res['general'] = None
	if len(temp) > 0:
		res['general'] = temp[0]
		temp[0]['saldo'] = temp[0]['In'] - temp[0]['Out']

	return res

def q_stok_stats(mode="MONTH"):
	res = {}

	c = connection.cursor()
	c.execute("select n.id, n.ktp, n.nama, n.alamat, n.telepon, n.tanggal_daftar, n.tanggal_lahir, coalesce(inning.total,0) as 'In', coalesce(outting.total,0) as 'Out' from transaction_nasabah n left outer join (select p.nasabah_id as id, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on s.id = ps.stok_id group by p.nasabah_id) as inning on n.id = inning.id left outer join (select n.id as id, sum(p.total) as total from transaction_nasabah n join transaction_penarikan p on n.id = p.nasabah_id group by n.id) as outting on n.id = outting.id where n.id=%s",[nasabah_id])
	temp = to_dict(c)
	return res

def q_laba_rugi(month, year):
	res = {}
	c = connection.cursor()
	c.execute("select dp.penjualan_id as id, p.tanggal as tanggal, sum(dp.harga*dp.jumlah) as bruto, sum(s.harga*dp.jumlah) as hpp FROM transaction_detailpenjualan dp JOIN transaction_stok_det s ON s.id = dp.stok_id JOIN transaction_penjualan p on dp.penjualan_id = p.id WHERE month(p.tanggal) = %s AND year(p.tanggal) = %s GROUP BY dp.penjualan_id ORDER BY dp.id", [month, year])
	res = to_dict(c)

	for r in res:
		r['netto'] = r['bruto'] - r['hpp']
	return res

def q_arus_barang(month, year):
	res = {}
	c = connection.cursor()
	# c.execute("select k.id, k.kode, k.nama, coalesce(i1.in_pembelian_individu,0) as in_pembelian_individu, coalesce(i1.in_pembelian_kolektif,0) as in_pembelian_kolektif, coalesce(i2.in_konversi,0) as in_konversi, coalesce(o1.out_penjualan,0) as out_penjualan, coalesce(o2.out_konversi,0) as out_konversi from transaction_kategori k left outer join (select s.kategori_id as kid, sum(case when n.jenis = 'individu' then s.jumlah else 0 end) as in_pembelian_individu, sum(case when n.jenis = 'kolektif' then s.jumlah else 0 end) as in_pembelian_kolektif from transaction_pembelian p, transaction_pembelian_stocks ps, transaction_stok s, transaction_nasabah n where p.id = ps.pembelian_id and s.id = ps.stok_id and n.id = p.nasabah_id and year(p.tanggal) = %s and month(p.tanggal) = %s group by s.kategori_id ) i1 on k.id = i1.kid left outer join (select s.kategori_id as kid, sum(s.jumlah) as in_konversi from transaction_konversi k, transaction_konversi_outs ok, transaction_stok s where k.id = ok.konversi_id and ok.stok_id = s.id and year(k.tanggal) = %s and month(k.tanggal) = %s group by s.kategori_id) i2 on k.id = i2.kid left outer join (select s.kategori_id as kid, sum(d.jumlah) as out_penjualan from transaction_konversi k, transaction_detailin d, transaction_stok s where k.id = d.konversi_id and d.stok_id = s.id and year(k.tanggal) = %s and month(k.tanggal) = %s group by s.kategori_id) o1 on k.id = o1.kid left outer join (select s.kategori_id as kid, sum(dp.jumlah) as out_konversi from transaction_penjualan p, transaction_detailpenjualan dp, transaction_stok s where p.id = dp.penjualan_id and dp.stok_id = s.id and year(p.tanggal) = %s and month(p.tanggal) = %s group by s.kategori_id) o2 on k.id = o2.kid", [year, month, year, month, year, month, year, month])
	c.execute("select kode, nama from transaction_kategori")

	kategori_list = to_dict(c)
	for k in kategori_list:
		res[k['kode']] = {'nama': k['nama'], 'penjualan': 0, 'pembelian_individu': 0, 'pembelian_kolektif':0, 'out_konversi':0, 'in_konversi':0}

	c.execute('select sd.kode as kode, sum(dp.jumlah) as jumlah from transaction_penjualan p, transaction_detailpenjualan dp,  transaction_stok_det sd where p.id = dp.penjualan_id and sd.id = dp.stok_id and	year(p.tanggal) = %s and month(p.tanggal) = %s group by sd.kode', [year, month])
	penjualan = to_dict(c)
	for p in penjualan:
		res[p['kode']]['penjualan'] = float(p['jumlah'])

	c.execute("select sd.kode as kode, sum(sd.jumlah) as jumlah from transaction_pembelian p, transaction_pembelian_stocks ps, transaction_stok_det sd, transaction_nasabah n where p.id = ps.pembelian_id and ps.stok_id = sd.id and p.nasabah_id = n.id and n.jenis = 'individu' and year(p.tanggal) = %s and month(p.tanggal) = %s group by sd.kode", [year, month])
	pembelian_individu = to_dict(c)
	for p in pembelian_individu:
		res[p['kode']]['pembelian_individu'] = float(p['jumlah'])

	c.execute("select sd.kode as kode, sum(sd.jumlah) as jumlah from transaction_pembelian p, transaction_pembelian_stocks ps, transaction_stok_det sd, transaction_nasabah n where p.id = ps.pembelian_id and ps.stok_id = sd.id and p.nasabah_id = n.id and n.jenis = 'kolektif' and year(p.tanggal) = %s and month(p.tanggal) = %s group by sd.kode", [year, month])
	pembelian_kolektif = to_dict(c)
	for p in pembelian_kolektif:
		res[p['kode']]['pembelian_kolektif'] = float(p['jumlah'])

	c.execute("select sd.kode as kode, sum(di.jumlah) as jumlah from transaction_konversi k, transaction_detailin di, transaction_stok_det sd where  k.id = di.konversi_id and di.stok_id = sd.id and year(k.tanggal)=%s and month(k.tanggal)=%s group by sd.kode", [year, month])
	in_konversi = to_dict(c)
	for p in in_konversi:
		res[p['kode']]['in_konversi'] = float(p['jumlah'])

	c.execute("select sd.kode as kode, sum(sd.jumlah) as jumlah from transaction_konversi k, transaction_konversi_outs ko, transaction_stok_det sd where k.id = ko.konversi_id and ko.stok_id = sd.id and year(k.tanggal) = %s and month(k.tanggal) = %s group by sd.kode", [year, month])
	out_konversi = to_dict(c)
	for p in out_konversi:
		res[p['kode']]['out_konversi'] = float(p['jumlah'])
	return res

def q_home():

	res = {}
	c = connection.cursor()

	#pembelian pertanggal
	c.execute("select p.tanggal, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on ps.stok_id = s.id group by p.tanggal order by p.tanggal")
	res['pembelian_pertanggal'] = to_dict(c)

	#pembelian hari ini
	c.execute("select p.tanggal, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on ps.stok_id = s.id where p.tanggal = DATE(NOW()) group by p.tanggal order by p.tanggal")
	res['pembelian_day'] = to_dict(c)

	#pembelian minggu ini
	c.execute("select p.tanggal, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on ps.stok_id = s.id where YEARWEEK(p.tanggal)=YEARWEEK(NOW()) group by p.tanggal order by p.tanggal")
	res['pembelian_week'] = to_dict(c)

	#pembelian bulan ini
	c.execute("select p.tanggal, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on ps.stok_id = s.id where MONTH(p.tanggal)=MONTH(NOW()) and YEAR(p.tanggal)=YEAR(NOW()) group by p.tanggal order by p.tanggal")
	res['pembelian_month'] = to_dict(c)

	#penjualan profit pertanggal
	c.execute("select p.tanggal, sum(dp.jumlah*dp.harga) as gross, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id group by p.tanggal order by p.tanggal")
	res['penjualan_pertanggal'] = to_dict(c)

	#Penjualan hari ini
	c.execute("select p.tanggal, sum(dp.jumlah*dp.harga) as gross, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id where p.tanggal = DATE(NOW()) group by p.tanggal order by p.tanggal")
	res['penjualan_day'] = to_dict(c)

	#Penjualan Minggu ini
	c.execute("select p.tanggal, sum(dp.jumlah*dp.harga) as gross, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id where YEARWEEK(p.tanggal)=YEARWEEK(NOW()) group by p.tanggal order by p.tanggal")
	res['penjualan_week'] = to_dict(c)

	#Penjualan Bulan ini
	c.execute("select p.tanggal, sum(dp.jumlah*dp.harga) as gross, sum(dp.jumlah*(dp.harga-s.harga)) as netto from transaction_detailpenjualan dp join transaction_penjualan p on dp.penjualan_id = p.id join transaction_stok_det s on s.id = dp.stok_id where MONTH(p.tanggal)=MONTH(NOW()) and YEAR(p.tanggal)=YEAR(NOW()) group by p.tanggal order by p.tanggal")
	res['penjualan_month'] = to_dict(c)

	#Stok week
	c.execute("select a.kode, a.in_konversi+a.in_pembelian as in_stok, b.out_konversi+b.out_penjualan as out_stok from (select k.kode, coalesce(in_konversi.jumlah,0) as in_konversi, coalesce(in_pembelian.jumlah,0) as in_pembelian from transaction_kategori k left outer join ( select sd.kode, sum(sd.jumlah) as jumlah from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id where YEARWEEK(k.tanggal)=YEARWEEK(NOW()) group by sd.kode ) in_konversi on k.kode = in_konversi.kode left outer join (select sd.kode, sum(sd.jumlah) as jumlah from  transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok_det sd on ps.stok_id = sd.id where YEARWEEK(p.tanggal)=YEARWEEK(NOW()) group by sd.kode) in_pembelian on k.kode = in_pembelian.kode) a join (select k.kode, coalesce(out_konversi.jumlah,0) as out_konversi, coalesce(out_penjualan.jumlah,0) as out_penjualan from transaction_kategori k left outer join ( select sd.kode, sum(d.jumlah) as jumlah from transaction_detailin d join transaction_konversi k on d.konversi_id = k.id join transaction_stok_det sd on d.stok_id = sd.id where YEARWEEK(k.tanggal)=YEARWEEK(NOW()) group by sd.kode ) out_konversi on k.kode = out_konversi.kode left outer join (select sd.kode, sum(dp.jumlah) as jumlah from transaction_detailpenjualan dp join transaction_penjualan p on p.id = dp.penjualan_id join transaction_stok_det sd on dp.stok_id = sd.id where YEARWEEK(p.tanggal)=YEARWEEK(NOW()) group by sd.kode) out_penjualan on k.kode = out_penjualan.kode) b on a.kode = b.kode")
	res['stok_week'] = to_dict(c)

	#Stok month
	c.execute("select a.kode, a.in_konversi+a.in_pembelian as in_stok, b.out_konversi+b.out_penjualan as out_stok from (select k.kode, coalesce(in_konversi.jumlah,0) as in_konversi, coalesce(in_pembelian.jumlah,0) as in_pembelian from transaction_kategori k left outer join ( select sd.kode, sum(sd.jumlah) as jumlah from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id where YEAR(k.tanggal)=YEAR(NOW()) and MONTH(k.tanggal)=MONTH(NOW()) group by sd.kode ) in_konversi on k.kode = in_konversi.kode left outer join (select sd.kode, sum(sd.jumlah) as jumlah from  transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok_det sd on ps.stok_id = sd.id where YEAR(p.tanggal)=YEAR(NOW()) and MONTH(p.tanggal)=MONTH(NOW()) group by sd.kode) in_pembelian on k.kode = in_pembelian.kode) a join (select k.kode, coalesce(out_konversi.jumlah,0) as out_konversi, coalesce(out_penjualan.jumlah,0) as out_penjualan from transaction_kategori k left outer join ( select sd.kode, sum(d.jumlah) as jumlah from transaction_detailin d join transaction_konversi k on d.konversi_id = k.id join transaction_stok_det sd on d.stok_id = sd.id where YEAR(k.tanggal)=YEAR(NOW()) and MONTH(k.tanggal)=MONTH(NOW()) group by sd.kode ) out_konversi on k.kode = out_konversi.kode left outer join (select sd.kode, sum(dp.jumlah) as jumlah from transaction_detailpenjualan dp join transaction_penjualan p on p.id = dp.penjualan_id join transaction_stok_det sd on dp.stok_id = sd.id where YEAR(p.tanggal)=YEAR(NOW()) and MONTH(p.tanggal)=MONTH(NOW()) group by sd.kode) out_penjualan on k.kode = out_penjualan.kode) b on a.kode = b.kode")
	res['stok_month'] = to_dict(c)

	#stok today
	c.execute("select a.kode, a.in_konversi+a.in_pembelian as in_stok, b.out_konversi+b.out_penjualan as out_stok from (select k.kode, coalesce(in_konversi.jumlah,0) as in_konversi, coalesce(in_pembelian.jumlah,0) as in_pembelian from transaction_kategori k left outer join ( select sd.kode, sum(sd.jumlah) as jumlah from transaction_konversi k join transaction_konversi_outs ko on k.id = ko.konversi_id join transaction_stok_det sd on ko.stok_id = sd.id where k.tanggal=DATE(NOW()) group by sd.kode ) in_konversi on k.kode = in_konversi.kode left outer join (select sd.kode, sum(sd.jumlah) as jumlah from  transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok_det sd on ps.stok_id = sd.id where p.tanggal=DATE(NOW()) group by sd.kode) in_pembelian on k.kode = in_pembelian.kode) a join (select k.kode, coalesce(out_konversi.jumlah,0) as out_konversi, coalesce(out_penjualan.jumlah,0) as out_penjualan from transaction_kategori k left outer join ( select sd.kode, sum(d.jumlah) as jumlah from transaction_detailin d join transaction_konversi k on d.konversi_id = k.id join transaction_stok_det sd on d.stok_id = sd.id where k.tanggal=DATE(NOW()) group by sd.kode ) out_konversi on k.kode = out_konversi.kode left outer join (select sd.kode, sum(dp.jumlah) as jumlah from transaction_detailpenjualan dp join transaction_penjualan p on p.id = dp.penjualan_id join transaction_stok_det sd on dp.stok_id = sd.id where p.tanggal=DATE(NOW()) group by sd.kode) out_penjualan on k.kode = out_penjualan.kode) b on a.kode = b.kode")
	res['stok_day'] = to_dict(c)

	#10 Penjualan terakhir
	res['10_penjualan'] = q_penjualan(limit=10)

	#10 Konversi terakhir
	res['10_konversi'] = q_konversi(limit=10)

	#10 Pembelian terakhir
	res['10_pembelian'] = q_pembelian(limit=10)

	#penarikan pertanggal
	c.execute("select p.tanggal, sum(p.total) as total from transaction_penarikan p group by p.tanggal order by p.tanggal")
	res['penarikan_pertanggal'] = to_dict(c)

	#10 penarikan terakhir
	c.execute("select p.id, p.tanggal, p.total as total from transaction_penarikan p order by p.tanggal desc limit 10")
	res['10_penarikan'] = to_dict(c)

	#Total Saldo
	c.execute("select sum(coalesce(inning.total,0)) as 'In', sum(coalesce(outting.total,0)) as 'Out' from transaction_nasabah n left outer join  (select p.nasabah_id as id, sum(s.jumlah*s.harga) as total from transaction_pembelian p join transaction_pembelian_stocks ps on p.id = ps.pembelian_id join transaction_stok s on s.id = ps.stok_id group by p.nasabah_id) as inning on n.id = inning.id left outer join (select n.id as id, sum(p.total) as total from transaction_nasabah n join transaction_penarikan p on n.id = p.nasabah_id group by n.id) as outting on n.id = outting.id")
	res['saldo'] = to_dict(c)
	res['saldo'][0]['saldo'] = (res['saldo'][0]['In'] or 0) - (res['saldo'][0]['Out'] or 0)

	#Total aset tertahan
	c.execute("select sr.*, k.stabil, k.fluktuatif from stok_remain sr join transaction_kategori k on k.kode=sr.kode where sisa > 0")
	res['aset'] = to_dict(c)

	res['aset_total'] = 0
	for r in res['aset']:
		res['aset_total'] += r['stabil']

	return res

def q_retrieve_pembelian_candidates(nasabah_id):
	all_pembelians = Pembelian.objects.filter(nasabah__id=nasabah_id)
	candidates_pembelians = []
	# import code
	# code.interact(local=dict(globals(), **locals()))

	for pembelian in all_pembelians:
		if pembelian.unsettled_value() > 0:
			candidates_pembelians.append(pembelian)

	return candidates_pembelians
