from django import forms 
from .models import Expense, Fund
from django.contrib.admin import widgets 
from django.core.exceptions import ValidationError  

from fund.models import Fund

class DateInput(forms.DateTimeInput):
	input_type='datetime-local'

class DateSelectorForm(forms.Form):
	date 		= forms.DateField(widget=DateInput)

class ExpenseAddForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		account = kwargs.pop('account')
		super(ExpenseAddForm, self).__init__(*args, **kwargs)
		self.fields['fund'].queryset = Fund.objects.filter(account=account)
		self.prev_instance = kwargs.pop('prev_instance')

	fund 		= forms.ModelChoiceField(queryset=None, initial=0)

	class Meta:
		model = Expense
		fields = [
			'description',
			'category',
			'price',
			'fund'
		]

	def clean_fund(self):
		price = self.cleaned_data['price']
		fund_obj = self.cleaned_data['fund']

		insufficient_balance = False
		if self.prev_instance is not None:
			prev_price = self.prev_instance.price
			prev_fund = self.prev_instance.fund
			if price > prev_price:
				insufficient_balance = (price - prev_price) > fund.amount
		else:
			insufficient_balance = fund.amount - price < 0

		if insufficient_balance:
			raise ValidationError(f'The fund {fund_obj.name} has insufficient balance\nCurrent Balance: {fund_obj.amount}')

		return fund_obj