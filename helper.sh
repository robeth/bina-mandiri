mysql -u root -p < recreate_db.sql
python manage.py syncdb
python manage.py migrate transaction
python manage.py runscript import_nasabah
python manage.py runscript import_initial_balance
python manage.py runscript import_initial_stock
python manage.py runscript import_initial_pembelian
