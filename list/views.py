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
		queryset = List.objects.filter(user=self.request.user).order_by('-timestamp')
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


###################################################################
# views for list entry
@method_decorator(login_required, name='dispatch')
class ListEntryCreateView(CreateView):
	model = ListEntry
	template_name = 'list_entry/create.html'
	success_url = reverse_lazy('list_entries_list')
	fields = ('content',)

	def form_valid(self, form):
		# get the list_id then check if exist, if so check if the current user is the owner of the list
		# object
		list_id = self.kwargs['list_id']
		try:
			list_obj = List.objects.get(pk=list_id)
		except LidtDoesNotExist:
			raise Http404()
		# check if the current user is the owner of the list object
		if list_obj.user != self.request.user:
			raise Http404()
		form.instance.list_obj = list_obj
		return super(ListEntryCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ListEntryListView(ListView):
	model = ListEntry
	template_name = 'list_entry/list.html'
	context_object_name = 'list_entries'
	paginate_by = 10

	def get_queryset(self):
		list_obj = self.get_list_object()

		queryset = ListEntry.objects.filter(list_obj=list_obj).order_by('-timestamp')
		return queryset

	def get_context_data(self, **kwargs):
		list_obj = self.get_list_object()
		context = super(ListEntryListView, self).get_context_data(**kwargs)
		list_entries = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(list_entries, self.paginate_by)

		list_entries = context['list_entries']
		detail_links = [reverse_lazy('list_entry_detail', kwargs={'pk':list_entry.pk, 'list_id':list_obj.id}) for list_entry in list_entries]
		try:
			list_entries = paginator.page(page)
		except PageNotAnInteger:
			list_entries = paginator.page(1)
		except EmptyPage:
			list_entries = paginator.page(paginator.num_pages)
		context['list_entry_details'] = zip(list_entries, detail_links)
		context['add_list_entry_link'] = reverse_lazy('list_entry_create', kwargs={'list_id':list_obj.id})
		context['go_home_link'] = reverse_lazy('home')
		return context

	def get_list_object(self):
		# get the list_id then check if exist, if so check if the current user is the owner of the list
		# object
		list_id = self.kwargs['list_id']
		try:
			list_obj = List.objects.get(pk=list_id)
		except LidtDoesNotExist:
			raise Http404()
		# check if the current user is the owner of the list object
		if list_obj.user != self.request.user:
			raise Http404()
		return list_obj


@method_decorator(login_required, name='dispatch')
class ListEntryDetailView(DetailView):
	model = ListEntry
	template_name = 'list_entry/detail.html'
	context_object_name = 'list_entry'

	def get_object(self, queryset=None):
		# get the current list object
		list_obj = self.get_list_object()
		obj = super(ListEntryDetailView, self).get_object(queryset=queryset)
		# check if the current list entry object is not owned by the list obj
		if obj.list_obj != list_obj:
			raise Http404()
		return obj

	def get_queryset(self):
		list_obj = self.get_list_object()
		queryset = super(ListEntryDetailView, self).get_queryset()
		return queryset.filter(list_obj=list_obj)

	def get_context_data(self, **kwargs):
		list_obj = self.get_list_object()
		context = super(ListEntryDetailView, self).get_context_data(**kwargs)
		list_entry = context['list_entry']
		delete_link = reverse_lazy('list_entry_delete', kwargs={'pk':list_entry.pk, 'list_id':list_obj.id})
		update_link = reverse_lazy('list_entry_update', kwargs={'pk':list_entry.pk, 'list_id':list_obj.id})
		context['delete_link'] = delete_link
		context['update_link'] = update_link
		context['go_back_link'] = reverse_lazy('list_entries_list', kwargs={'list_id':list_obj.id})
		return context

	def get_list_object(self):
		# get the list_id then check if exist, if so check if the current user is the owner of the list
		# object
		list_id = self.kwargs['list_id']
		try:
			list_obj = List.objects.get(pk=list_id)
		except LidtDoesNotExist:
			raise Http404()
		# check if the current user is the owner of the list object
		if list_obj.user != self.request.user:
			raise Http404()
		return list_obj


@method_decorator(login_required, name='dispatch')
class ListEntryUpdateView(UpdateView):
	model = ListEntry 
	template_name = 'list_entry/update.html'
	context_object_name = 'list_entry'
	fields = ('content',)

	def get_success_url(self):
		list_obj = self.get_list_object()
		return reverse_lazy('list_entry_detail', kwargs={'pk':self.object.id, 'list_id':list_obj.id})

	def get_object(self, queryset=None):
		list_obj = self.get_list_object()
		obj = super(ListEntryUpdateView, self).get_object(queryset=queryset)
		# check if the current list entry is owned by the list object
		if obj.list_obj != list_obj:
			raise Http404()
		return obj

	def get_queryset(self):
		list_obj = self.get_list_object()
		queryset = super(ListEntryUpdateView, self).get_queryset()
		return queryset.filter(list_obj=list_obj)

	def get_list_object(self):
		# get the list_id then check if exist, if so check if the current user is the owner of the list
		# object
		list_id = self.kwargs['list_id']
		try:
			list_obj = List.objects.get(pk=list_id)
		except LidtDoesNotExist:
			raise Http404()
		# check if the current user is the owner of the list object
		if list_obj.user != self.request.user:
			raise Http404()
		return list_obj

@method_decorator(login_required, name='dispatch')
class ListEntryDeleteView(DeleteView):
	model = ListEntry
	template_name = 'list_entry/delete.html'

	def get_success_url(self):
		list_obj = self.get_list_object()
		return reverse_lazy('list_entry_detail', kwargs={'pk':self.object.id, 'list_id':list_obj.id})

	def get_object(self, queryset=None):
		list_obj = self.get_list_object()
		obj = super(ListEntryDeleteView, self).get_object(queryset=queryset)
		# check if the current list entry is owned by the list object
		if obj.list_obj != list_obj:
			raise Http404()
		return obj

	def get_queryset(self):
		list_obj = self.get_list_object()
		queryset = super(ListEntryDeleteView, self).get_queryset()
		return queryset.filter(list_obj=list_obj)

	def get_list_object(self):
		# get the list_id then check if exist, if so check if the current user is the owner of the list
		# object
		list_id = self.kwargs['list_id']
		try:
			list_obj = List.objects.get(pk=list_id)
		except LidtDoesNotExist:
			raise Http404()
		# check if the current user is the owner of the list object
		if list_obj.user != self.request.user:
			raise Http404()
		return list_obj
