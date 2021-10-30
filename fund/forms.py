from django import forms

class FundAllocationForm(forms.Form):
	ACTIONS = (
		('AL', 'Allocate'),
		('DL', 'Deallocate'))

	amount 			= forms.IntegerField()
	action 			= forms.CharField(max_length=2, choices=ACTIONS)