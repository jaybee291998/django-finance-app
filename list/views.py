from datetime import date, datetime, timedelta
import random

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


from .models import List, ListEntry

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListCreateView(CreateView):
	model = List
	template_name = 'list/create.html'
	success_url = reverse_lazy('lists_list')
	fields = ('title', 'description')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ListCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ListListView(ListView):
	model = List
	template_name = 'list/list.html'
	context_object_name = 'lists'
	paginate_by = 10

	def get_queryset(self):
		queryset = List.objects.filter(user=self.request.user)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ListListView, self).get_context_data(**kwargs)
		lists = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(lists, self.paginate_by)

		lists = context['lists']
		detail_links = [reverse_lazy('list_detail', kwargs={'pk':list_obj.pk}) for list_obj in lists]
		try:
			lists = paginator.page(page)
		except PageNotAnInteger:
			lists = paginator.page(1)
		except EmptyPage:
			lists = paginator.page(paginator.num_pages)
		context['list_details'] = zip(lists, detail_links)
		context['add_list_link'] = reverse_lazy('list_create')
		context['go_home_link'] = reverse_lazy('home')
		return context

@method_decorator(login_required, name='dispatch')
class ListDetailView(DetailView):
	model = List
	template_name = 'list/detail.html'
	context_object_name = 'list'

	def get_object(self, queryset=None):
		obj = super(ListDetailView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(ListDetailView, self).get_queryset()
		return queryset.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(ListDetailView, self).get_context_data(**kwargs)
		list_obj = context['list']
		delete_link = reverse_lazy('list_delete', kwargs={'pk':list_obj.pk})
		update_link = reverse_lazy('list_update', kwargs={'pk':list_obj.pk})
		context['delete_link'] = delete_link
		context['update_link'] = update_link
		context['go_back_link'] = reverse_lazy('lists_list')
		return context


@method_decorator(login_required, name='dispatch')
class ListUpdateView(UpdateView):
	model = List 
	template_name = 'list/update.html'
	context_object_name = 'list'
	fields = ('title', 'description')

	def get_success_url(self):
		return reverse_lazy('list_detail', kwargs={'pk':self.object.id})

	def get_object(self, queryset=None):
		obj = super(ListUpdateView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(ListUpdateView, self).get_queryset()
		return queryset.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class ListDeleteView(DeleteView):
	model = List
	template_name = 'list/delete.html'
	success_url = reverse_lazy('lists_list')

	def get_object(self, queryset=None):
		obj = super(ListDeleteView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(ListDeleteView, self).get_queryset()
		return queryset.filter(user=self.request.user)
