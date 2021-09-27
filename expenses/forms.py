from django import forms 
from .models import Expense, Fund
from django.contrib.admin import widgets   

class DateInput(forms.DateTimeInput):
	input_type='datetime-local'

class DateSelectorForm(forms.Form):
	date 		= forms.DateField(widget=DateInput)

class ExpenseAddForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		account = kwargs.pop('account')
		super(ExpenseAddForm, self).__init__(*args, **kwargs)
		self.fields['fund'].queryset = Fund.objects.filter(account=account)

	fund 		= forms.ModelChoiceField(queryset=None, initial=0)

	class Meta:
		model = Expense
		fields = [
			'description',
			'category',
			'price',
			'fund'
		]
