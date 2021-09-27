from datetime import date, datetime, timedelta
import random

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy

from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


from .models import Income

from accounts.utils import is_object_expired
from expenses.forms import DateSelectorForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class IncomeCreateView(CreateView):
	model = Income
	template_name = 'income/create.html'
	success_url = reverse_lazy('incomes_list')
	fields = ('description', 'category', 'amount', 'source')

	def form_valid(self, form):
		form.instance.account = self.request.user.bank_account
		return super(IncomeCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class IncomeListView(ListView):
	model = Income
	template_name = 'income/list.html'
	context_object_name = 'incomes'
	paginate_by = 10

	def get_queryset(self):
		entry_date = date.today()

		if self.request.GET:
			entry_date = datetime.strptime(self.request.GET['date'][:10].replace('-',''), "%Y%m%d").date()

		queryset = Income.objects.filter(account=self.request.user.bank_account, timestamp__year=entry_date.year, timestamp__month=entry_date.month, timestamp__day=entry_date.day).order_by('-timestamp')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(IncomeListView, self).get_context_data(**kwargs)
		incomes = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(incomes, self.paginate_by)

		incomes = context['incomes']
		detail_links = [reverse_lazy('income_detail', kwargs={'pk':income.pk}) for income in incomes]
		total_income = sum([income.amount for income in incomes])
		entry_date = datetime.strptime(self.request.GET['date'][:10].replace('-',''), "%Y%m%d").date() if self.request.GET else date.today()

		try:
			incomes = paginator.page(page)
		except PageNotAnInteger:
			incomes = paginator.page(1)
		except EmptyPage:
			incomes = paginator.page(paginator.num_pages)
		context['income_details'] = zip(incomes, detail_links)
		context['add_income_link'] = reverse_lazy('income_create')
		context['go_home_link'] = reverse_lazy('home')
		context['total_income'] = total_income
		context['entry_date'] = entry_date
		context['form'] = DateSelectorForm()
		return context

@method_decorator(login_required, name='dispatch')
class IncomeDetailView(DetailView):
	model = Income
	template_name = 'income/detail.html'
	context_object_name = 'income'

	def get_object(self, queryset=None):
		obj = super(IncomeDetailView, self).get_object(queryset=queryset)
		if obj.account != self.request.user.bank_account:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(IncomeDetailView, self).get_queryset()
		return queryset.filter(account=self.request.user.bank_account)

	def get_context_data(self, **kwargs):
		context = super(IncomeDetailView, self).get_context_data(**kwargs)
		income = context['income']
		delete_link = reverse_lazy('income_delete', kwargs={'pk':income.pk})
		update_link = reverse_lazy('income_update', kwargs={'pk':income.pk})
		# check if the object is already expired
		if not is_object_expired(income, settings.TWELVE_HOUR_DURATION):
			context['update_link'] = update_link
			context['delete_link'] = delete_link
			context['is_expired'] = False
		else:
			context['is_expired'] = True
		context['go_back_link'] = reverse_lazy('incomes_list')
		return context


@method_decorator(login_required, name='dispatch')
class IncomeUpdateView(UpdateView):
	model = Income
	template_name = 'income/update.html'
	context_object_name = 'income'
	fields = ('description', 'category', 'amount', 'source')

	def get_success_url(self):
		return reverse_lazy('income_detail', kwargs={'pk':self.object.id})

	def get_object(self, queryset=None):
		obj = super(IncomeUpdateView, self).get_object(queryset=queryset)
		if obj.account != self.request.user.bank_account:
			raise Http404()
		if is_object_expired(obj, settings.TWELVE_HOUR_DURATION):
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(IncomeUpdateView, self).get_queryset()
		return queryset.filter(account=self.request.user.bank_account)

@method_decorator(login_required, name='dispatch')
class IncomeDeleteView(DeleteView):
	model = Income
	template_name = 'income/delete.html'
	success_url = reverse_lazy('incomes_list')

	def get_object(self, queryset=None):
		obj = super(IncomeDeleteView, self).get_object(queryset=queryset)
		if obj.account != self.request.user.bank_account:
			raise Http404()
		if is_object_expired(obj, settings.TWELVE_HOUR_DURATION):
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(IncomeDeleteView, self).get_queryset()
		return queryset.filter(account=self.request.user.bank_account)
