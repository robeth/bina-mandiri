# BSBM

A Django web application developed for [Bank Sampah Bina Mandiri](http://www.banksampahbinamandiri.com/). Eventhough it is a web appplication, this project is designed for personal/localhost use. 

Was dreamed to replace Microsoft Excel usage, help operation team finish workflow easier and faster.

Contributions is really appreciated :)

# Main feature

1. Record
    - Asset
    - Customer
    - Vendor
    - Activity (Penjualan, Pembelian, Konversi)
2. Report
    - Profit/loss
    - Summary

# Getting Started

1. Requirement
    - [Python 2.7](https://www.python.org/download/releases/2.7/)
    - [Pip](https://pip.pypa.io/en/latest/installing.html)
    - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (recommended)
    - [MySQL Server](http://dev.mysql.com/downloads/mysql/)

2. Clone application and enter folder
    
        git clone https://github.com/robeth/bina-mandiri.git bsm

        cd bsm/

3. Change database config in bsm/settings.py

        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bsm',
            'USER': '[your mysql user]',
            'PASSWORD': '[yout mysql password]',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }    

4. Start virtualenv

        virtualenv ENV
        source ENV/bin/activate


5. Download python package dependencies

        pip install -r requirements.txt

6. Database migration

        python manage.py migrate transaction

7. Run server

        python manage.py runserver

8. Visit localhost:8000
