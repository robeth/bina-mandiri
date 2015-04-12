# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Nasabah'
        db.create_table(u'transaction_nasabah', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ktp', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('alamat', self.gf('django.db.models.fields.TextField')()),
            ('telepon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('tanggal_lahir', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tanggal_daftar', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('jenis', self.gf('django.db.models.fields.CharField')(default='individu', max_length=20)),
        ))
        db.send_create_signal(u'transaction', ['Nasabah'])

        # Adding model 'Vendor'
        db.create_table(u'transaction_vendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('alamat', self.gf('django.db.models.fields.TextField')()),
            ('telepon', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('tanggal_daftar', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'transaction', ['Vendor'])

        # Adding model 'Kategori'
        db.create_table(u'transaction_kategori', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('deskripsi', self.gf('django.db.models.fields.TextField')()),
            ('satuan', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('stabil', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('fluktuatif', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'transaction', ['Kategori'])

        # Adding model 'Stok'
        db.create_table(u'transaction_stok', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kategori', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Kategori'])),
            ('tanggal', self.gf('django.db.models.fields.DateField')()),
            ('jumlah', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('harga', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'transaction', ['Stok'])

        # Adding model 'Pembelian'
        db.create_table(u'transaction_pembelian', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nasabah', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Nasabah'])),
            ('tanggal', self.gf('django.db.models.fields.DateField')()),
            ('nota', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'transaction', ['Pembelian'])

        # Adding M2M table for field stocks on 'Pembelian'
        m2m_table_name = db.shorten_name(u'transaction_pembelian_stocks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pembelian', models.ForeignKey(orm[u'transaction.pembelian'], null=False)),
            ('stok', models.ForeignKey(orm[u'transaction.stok'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pembelian_id', 'stok_id'])

        # Adding model 'Penjualan'
        db.create_table(u'transaction_penjualan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Vendor'])),
            ('tanggal', self.gf('django.db.models.fields.DateField')()),
            ('nota', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'transaction', ['Penjualan'])

        # Adding model 'DetailPenjualan'
        db.create_table(u'transaction_detailpenjualan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('penjualan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Penjualan'])),
            ('stok', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Stok'])),
            ('jumlah', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('harga', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'transaction', ['DetailPenjualan'])

        # Adding model 'Konversi'
        db.create_table(u'transaction_konversi', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tanggal', self.gf('django.db.models.fields.DateField')()),
            ('kode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'transaction', ['Konversi'])

        # Adding M2M table for field outs on 'Konversi'
        m2m_table_name = db.shorten_name(u'transaction_konversi_outs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('konversi', models.ForeignKey(orm[u'transaction.konversi'], null=False)),
            ('stok', models.ForeignKey(orm[u'transaction.stok'], null=False))
        ))
        db.create_unique(m2m_table_name, ['konversi_id', 'stok_id'])

        # Adding model 'DetailIn'
        db.create_table(u'transaction_detailin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('konversi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Konversi'])),
            ('stok', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Stok'])),
            ('jumlah', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal(u'transaction', ['DetailIn'])

        # Adding model 'Penarikan'
        db.create_table(u'transaction_penarikan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nasabah', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.Nasabah'])),
            ('tanggal', self.gf('django.db.models.fields.DateField')()),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('nota', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'transaction', ['Penarikan'])


    def backwards(self, orm):
        # Deleting model 'Nasabah'
        db.delete_table(u'transaction_nasabah')

        # Deleting model 'Vendor'
        db.delete_table(u'transaction_vendor')

        # Deleting model 'Kategori'
        db.delete_table(u'transaction_kategori')

        # Deleting model 'Stok'
        db.delete_table(u'transaction_stok')

        # Deleting model 'Pembelian'
        db.delete_table(u'transaction_pembelian')

        # Removing M2M table for field stocks on 'Pembelian'
        db.delete_table(db.shorten_name(u'transaction_pembelian_stocks'))

        # Deleting model 'Penjualan'
        db.delete_table(u'transaction_penjualan')

        # Deleting model 'DetailPenjualan'
        db.delete_table(u'transaction_detailpenjualan')

        # Deleting model 'Konversi'
        db.delete_table(u'transaction_konversi')

        # Removing M2M table for field outs on 'Konversi'
        db.delete_table(db.shorten_name(u'transaction_konversi_outs'))

        # Deleting model 'DetailIn'
        db.delete_table(u'transaction_detailin')

        # Deleting model 'Penarikan'
        db.delete_table(u'transaction_penarikan')


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