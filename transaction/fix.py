from transaction.models import Penjualan, Konversi, DetailPenjualan, DetailIn, Vendor, Stok, Kategori
from transaction.db import q_get_last_stock
from operator import itemgetter

def redo():
	penjualan_db = Penjualan.objects.all();
	konversi_db = Konversi.objects.all();

	counter = 1
	# Populate sales data
	action_penjualan_temp = []
	for p_db in penjualan_db:
		print "Export Penjualan - " + str(counter)
		p_temp = {
				'type' : 'penjualan',
				'id' : p_db.id,
				'vendor_id' : p_db.vendor_id,
				'tanggal' : p_db.tanggal,
				'nota' : p_db.nota,
				'stocks' : {}
			}

		# Populate sales items
		p_stocks_temp = {}
		for p_stock_db in p_db.detailpenjualan_set.all():
			item_id = p_stock_db.stok.kategori.kode + "-" +str(p_stock_db.harga)
			if item_id in p_stocks_temp:
				p_stocks_temp[item_id]['jumlah'] += p_stock_db.jumlah
			else:
				p_stocks_temp[item_id] = {
					'kode' : p_stock_db.stok.kategori.kode,
					'jumlah' : p_stock_db.jumlah,
					'harga' : p_stock_db.harga
					}
		p_temp['stocks'] = p_stocks_temp

		# Append current sales
		action_penjualan_temp.append(p_temp)

		counter += 1

	# Populate konversi data
	counter = 1
	action_konversi_temp = []
	for k_db in konversi_db:
		print "Export konversi - " + str(counter)
		k_temp = {
				'type' : 'konversi',
				'id' : k_db.id,
				'tanggal' : k_db.tanggal,
				'kode' : k_db.kode,
				'stocks_in' : {},
				'stocks_out' : {}
			}
		# Populate in data
		k_stocks_in_temp = {}
		for k_stock_in_db in k_db.detailin_set.all():
			item_id = k_stock_in_db.stok.kategori.kode
			if item_id in k_stocks_in_temp:
				k_stocks_in_temp[item_id]['jumlah'] += k_stock_in_db.jumlah
			else:
				k_stocks_in_temp[item_id] = {
						'jumlah' : k_stock_in_db.jumlah
					}

		# Populate out data
		k_stocks_out_temp = {}
		for k_stock_out_db in k_db.outs.all():
			item_id = k_stock_out_db.kategori.kode
			if item_id in k_stocks_out_temp:
				k_stocks_out_temp[item_id]['jumlah'] += k_stock_out_db.jumlah
			else:
				k_stocks_out_temp[item_id] = {
						'jumlah' : k_stock_out_db.jumlah
					}

		k_temp['stocks_in'] = k_stocks_in_temp
		k_temp['stocks_out'] = k_stocks_out_temp

		# Append current konversi data
		action_konversi_temp.append(k_temp)

		counter += 1

	sorted_action_penjualan_temp = sorted(action_penjualan_temp, key=itemgetter('id'))
	sorted_action_konversi_temp = sorted(action_konversi_temp, key=itemgetter('id'))
	# print "Before sort: "
	# print10(action_temp)
	# print "After sort:"
	# print10(sorted_action_temp)

	all_sales = Penjualan.objects.all()
	all_konversi = Konversi.objects.all()
	all_stok = Stok.objects.all()

	print "Delete all konversi output"
	for kk in all_konversi:
		kk.outs.all().delete()

	# print "Delete orphan stok"
	# for stok_item in all_stok:
	# 	if not stok_item.pembelian_set.all():
	# 		stok_item.delete()

	all_sales.delete()
	all_konversi.delete()

	counter = 1
	for data in sorted_action_konversi_temp:
		print "Import Konversi- " + str(counter)
		counter += 1
		if data['type'] == 'konversi':
			k = Konversi(id=data['id'],tanggal=data['tanggal'], kode=data['kode'])
			k.save()

			total_nilai = 0
			total_jumlah = 0
			harga_satuan = 0

			for key, in_item in data['stocks_in'].iteritems():
				stocks = q_get_last_stock(key, in_item['jumlah'])
				for s in stocks:
					st = Stok.objects.get(id=s['id'])
					total_nilai += float(st.harga) * float(s['jumlah'])
					# print "total_nilai: "+str(float(st.harga)) + " * " + str(float(data['jumlah_in'+str(i)]))
					di = DetailIn(stok=st, konversi=k, jumlah=s['jumlah'])
					di.save()

			for key, out_item in data['stocks_out'].iteritems():
				total_jumlah += float(out_item['jumlah'])

			if total_jumlah == 0:
				harga_satuan = 0
			else:
				harga_satuan = total_nilai / total_jumlah
			# print "satuan:" + str(harga_satuan)
			# print "total nilai:" + str(total_nilai)
			# print "total jumlah" + str(total_jumlah)
			
			for key, out_item in data['stocks_out'].iteritems():
				kk = Kategori.objects.get(kode=key)
				s = Stok(kategori = kk,
						tanggal = data['tanggal'],
						jumlah = float(out_item['jumlah']),
						harga = harga_satuan)

				s.save()
				k.outs.add(s)
			k.save()

	counter = 1
	for data in sorted_action_penjualan_temp:
		print "Import Penjualan- " + str(counter)
		counter += 1
		if data['type'] == 'penjualan':
			v = Vendor.objects.get(id=data['vendor_id'])
			p = Penjualan(id=data['id'],tanggal=data['tanggal'], vendor = v, nota=data['nota'])
			p.save()

			for key, item in data['stocks'].iteritems():
				stocks = q_get_last_stock(item['kode'], item['jumlah'])
				for s in stocks:
					st = Stok.objects.get(id=s['id'])
					dp = DetailPenjualan(stok=st, penjualan=p, jumlah=s['jumlah'], harga=item['harga'])
					dp.save()