from django import forms
from django.forms import ModelForm
from transaction.models import Nasabah, Vendor, Pembelian, Kategori, Penjualan, Konversi, Penarikan
from transaction.db import q_remaining_dict, q_nasabah_detail_only, q_reclaimed_stocks

class NasabahForm(ModelForm):
	class Meta:
		model = Nasabah
		exclude = ('tanggal_daftar',)

class LoginForm(ModelForm):
	class Meta:
		model = Nasabah
		exclude = ('tanggal_daftar',)

class KategoriForm(ModelForm):
	class Meta:
		model = Kategori

class VendorForm(ModelForm):
	class Meta:
		model = Vendor
		exclude = ('tanggal_daftar',)
	def clean(self):
		cleaned_data = super(VendorForm, self).clean()
		c_nama = cleaned_data.get('nama')

		if 'Robeth' in c_nama:
			raise forms.ValidationError('Dont include Robeth in your name please :)')

		return cleaned_data

class PembelianForm(ModelForm):
	class Meta:
		model = Pembelian
		exclude = ('stocks',)

	def clean(self):
		cleaned_data = super(PembelianForm, self).clean()
		data = self.data

		if 'total' in data:
			limit = int(data['total'])
			i = 1
			while i <= limit:
				try:
					temp = Kategori.objects.get(id=data['stok'+str(i)])
				except Kategori.DoesNotExist :
					raise forms.ValidationError('Kategori '+ str(i)+ ' Does Not Exist')
				i += 1

			return cleaned_data
		else:
			raise forms.ValidationError('Total variable is not defined!')

class PenjualanForm(ModelForm):
	class Meta:
		model = Penjualan
		exclude = ('stocks',)
	def clean(self):
		cleaned_data = super(PenjualanForm, self).clean()
		data = self.data
		remaining = q_remaining_dict()

		if 'penjualan_id' in data:
			reclaimed_stocks = q_reclaimed_stocks(data['penjualan_id'])
			for k,v in reclaimed_stocks.iteritems():
				remaining[k]['jumlah_penjualan'] -= v
				remaining[k]['sisa'] += v
				
		if 'total' in data:
			limit = int(data['total'])
			i = 1
			while i <= limit:
				try:
					temp = Kategori.objects.get(kode=data['stok'+str(i)])
					if (float(data['jumlah'+str(i)]) > float(remaining[data['stok'+str(i)]]['sisa'])):
						raise forms.ValidationError('Kategori '+ data['stok'+str(i)]+ ' Insufficient. Stok:' + str(float(remaining[data['stok'+str(i)]]['sisa'])))
				except Kategori.DoesNotExist :
					raise forms.ValidationError('Kategori '+ str(i)+ ' Does Not Exist')
				except Exception as e:
					raise forms.ValidationError(str(e))
				i += 1

			return cleaned_data
		else:
			raise forms.ValidationError('Total variable is not defined!')

class KonversiForm(ModelForm):
	class Meta:
		model = Konversi
		exclude = ('ins', 'outs')

	def clean(self):
		cleaned_data = super(KonversiForm, self).clean()
		data = self.data
		remaining = q_remaining_dict()

		if 'total' in data:
			limit = int(data['total'])
			i = 1
			while i <= limit:
				try:
					temp = Kategori.objects.get(kode=data['stok_in'+str(i)])
					if (float(data['jumlah_in'+str(i)]) > float(remaining[data['stok_in'+str(i)]]['sisa'])):
						raise forms.ValidationError('Kategori '+ data['stok_in'+str(i)]+ ' Insufficient. Stok:' + str(float(remaining[data['stok_in'+str(i)]]['sisa'])))
				except Kategori.DoesNotExist :
					raise forms.ValidationError('Kategori '+ str(i)+ ' Does Not Exist')
				i += 1

			return cleaned_data
		else:
			raise forms.ValidationError('Total variable is not defined!')


class PenarikanForm(ModelForm):
	class Meta:
		model = Penarikan

	pembelians = forms.ModelMultipleChoiceField(queryset=None)
	
	def __init__(self, nasabah_id, *args, **kw):
		instance = kw.get('instance', None)
		
		# Set existing pembelians selected 
		if instance:
			kw.update(initial={
					'pembelians': [unicode(p.id) for p in instance.pembelian_set.all()]
				})
		super(PenarikanForm, self).__init__(*args, **kw)
		
		# Choice based on unpaid pembelians and existing pembelians(if any)
		queryset_pembelians = Nasabah.objects.get(id=nasabah_id).pembelian_set.filter(penarikan_id__isnull=True)
		if instance:
			current_pembelians = kw['instance'].pembelian_set.all()
			queryset_pembelians = queryset_pembelians | current_pembelians

		# import code
		# code.interact(local=dict(globals(), **locals()))
		self.fields['nasabah'] = forms.ModelChoiceField(queryset=Nasabah.objects.filter(id=nasabah_id), initial=0)
		self.fields['pembelians'] = forms.ModelMultipleChoiceField(
			queryset=queryset_pembelians,
			widget=forms.CheckboxSelectMultiple)


	def clean(self):
		cleaned_data = super(PenarikanForm, self).clean()
		if cleaned_data.get('pembelians'):
			cleaned_data['total'] = sum([p.total_value() for p in cleaned_data.get('pembelians')])
		
		nasabah_id = cleaned_data.get('nasabah')
		total = float(cleaned_data.get('total'))

		res = q_nasabah_detail_only(nasabah_id)

		if res['general']:
			if float(res['general']['saldo']) < total:
				self._errors['total'] = self.error_class([u'Saldo tidak mencukupi'])
				del cleaned_data['total']

		return cleaned_data