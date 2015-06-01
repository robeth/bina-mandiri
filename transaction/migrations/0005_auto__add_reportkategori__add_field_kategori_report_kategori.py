# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportKategori'
        db.create_table(u'transaction_reportkategori', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('satuan', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'transaction', ['ReportKategori'])

        # Adding field 'Kategori.report_kategori'
        db.add_column(u'transaction_kategori', 'report_kategori',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['transaction.ReportKategori']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ReportKategori'
        db.delete_table(u'transaction_reportkategori')

        # Deleting field 'Kategori.report_kategori'
        db.delete_column(u'transaction_kategori', 'report_kategori_id')


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