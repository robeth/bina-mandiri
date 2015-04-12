# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


def run_file(file_name):
        import os
        f = open(os.path.join(os.path.dirname(__file__), file_name))
        query = f.read()
        db.execute(query)

class Migration(SchemaMigration):

    def forwards(self, orm):
        run_file('sql/002_view_01_transaction_stok_det.sql')
        run_file('sql/002_view_02_transaction_penjualan_total.sql')
        run_file('sql/002_view_03_transaction_penjualan_recap.sql')
        run_file('sql/002_view_04_transaction_pembelian_total.sql')
        run_file('sql/002_view_05_transaction_pembelian_recap.sql')
        run_file('sql/002_view_06_transaction_in_stok.sql')
        run_file('sql/002_view_07_transaction_out_konversi.sql')
        run_file('sql/002_view_08_transaction_out_penjualan.sql')
        run_file('sql/002_view_09_stok_remain.sql')


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")