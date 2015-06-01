# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        default_report_kategori = orm.ReportKategori(id=1,nama="Lain-Lain", satuan="unit")
        logam_report_kategori = orm.ReportKategori(nama="Logam", satuan="kg")
        kaca_report_kategori = orm.ReportKategori(nama="Kaca", satuan="kg")
        plastik_lembar_report_kategori = orm.ReportKategori(nama="Plastik", satuan="kg")
        plastik_non_lembar_report_kategori = orm.ReportKategori(nama="Plastik non lembar", satuan="kg")
        kertas_report_kategori = orm.ReportKategori(nama="Kertas", satuan="kg")

        default_report_kategori.save()
        logam_report_kategori.save()
        kaca_report_kategori.save()
        plastik_lembar_report_kategori.save()
        plastik_non_lembar_report_kategori.save()
        kertas_report_kategori.save()

        al_kategori = orm.Kategori.objects.filter(kode__iregex=r'AL[0-9]+')
        bt_kategori = orm.Kategori.objects.filter(kode__iregex=r'BT[0-9]+')
        pl_kategori = orm.Kategori.objects.filter(kode__iregex=r'PL[0-9]+')
        p_kategori = orm.Kategori.objects.filter(kode__iregex=r'P[0-9]+')
        k_kategori = orm.Kategori.objects.filter(kode__iregex=r'K[0-9]+')

        for al_element in al_kategori:
            al_element.report_kategori = logam_report_kategori
            al_element.save()

        for bt_element in bt_kategori:
            bt_element.report_kategori = kaca_report_kategori
            bt_element.save()

        for pl_element in pl_kategori:
            pl_element.report_kategori = plastik_lembar_report_kategori
            pl_element.save()

        for p_element in p_kategori:
            p_element.report_kategori = plastik_non_lembar_report_kategori
            p_element.save()

        for k_element in k_kategori:
            k_element.report_kategori = kertas_report_kategori
            k_element.save()

    def backwards(self, orm):
        pass

    models = {
        u'transaction.detailin': {
            'Meta': {'object_name': 'DetailIn'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jumlah': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'konversi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Konversi']"}),
            'stok': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Stok']"})
        },
        u'transaction.detailpenjualan': {
            'Meta': {'object_name': 'DetailPenjualan'},
            'harga': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jumlah': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'penjualan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Penjualan']"}),
            'stok': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Stok']"})
        },
        u'transaction.kategori': {
            'Meta': {'object_name': 'Kategori'},
            'deskripsi': ('django.db.models.fields.TextField', [], {}),
            'fluktuatif': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'report_kategori': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['transaction.ReportKategori']"}),
            'satuan': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stabil': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'})
        },
        u'transaction.konversi': {
            'Meta': {'object_name': 'Konversi'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stock_in_id'", 'symmetrical': 'False', 'through': u"orm['transaction.DetailIn']", 'to': u"orm['transaction.Stok']"}),
            'kode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'outs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stock_out_id'", 'symmetrical': 'False', 'to': u"orm['transaction.Stok']"}),
            'tanggal': ('django.db.models.fields.DateField', [], {})
        },
        u'transaction.nasabah': {
            'Meta': {'object_name': 'Nasabah'},
            'alamat': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jenis': ('django.db.models.fields.CharField', [], {'default': "'individu'", 'max_length': '20'}),
            'ktp': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tanggal_daftar': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'tanggal_lahir': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'telepon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'transaction.pembelian': {
            'Meta': {'object_name': 'Pembelian'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nasabah': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Nasabah']"}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'penarikan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Penarikan']", 'null': 'True', 'blank': 'True'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['transaction.Stok']", 'symmetrical': 'False'}),
            'tanggal': ('django.db.models.fields.DateField', [], {})
        },
        u'transaction.penarikan': {
            'Meta': {'object_name': 'Penarikan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nasabah': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Nasabah']"}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tanggal': ('django.db.models.fields.DateField', [], {}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'})
        },
        u'transaction.penjualan': {
            'Meta': {'object_name': 'Penjualan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['transaction.Stok']", 'through': u"orm['transaction.DetailPenjualan']", 'symmetrical': 'False'}),
            'tanggal': ('django.db.models.fields.DateField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Vendor']"})
        },
        u'transaction.reportkategori': {
            'Meta': {'object_name': 'ReportKategori'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'satuan': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'transaction.stok': {
            'Meta': {'object_name': 'Stok'},
            'harga': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jumlah': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'kategori': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.Kategori']"}),
            'tanggal': ('django.db.models.fields.DateField', [], {})
        },
        u'transaction.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'alamat': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tanggal_daftar': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'telepon': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['transaction']