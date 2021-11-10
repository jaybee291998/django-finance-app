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


from .models import Diary
from .serializers import DiarySerializer

from expenses.forms import DateSelectorForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DiaryCreateView(CreateView):
	model = Diary
	template_name = 'diary/create.html'
	success_url = reverse_lazy('diaries_list')
	fields = ('title', 'content')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(DiaryCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class DiaryListView(ListView):
	model = Diary
	template_name = 'diary/list.html'
	context_object_name = 'diaries'
	paginate_by = 10

	def get_queryset(self):
		entry_date = date.today()

		if self.request.GET:
			entry_date = datetime.strptime(self.request.GET['date'][:10].replace('-',''), "%Y%m%d").date()

		queryset = Diary.objects.filter(user=self.request.user, timestamp__year=entry_date.year, timestamp__month=entry_date.month, timestamp__day=entry_date.day).order_by('-timestamp')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(DiaryListView, self).get_context_data(**kwargs)
		diaries = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(diaries, self.paginate_by)

		diaries = context['diaries']
		detail_links = [reverse_lazy('diary_detail', kwargs={'pk':diary.pk}) for diary in diaries]
		entry_date = datetime.strptime(self.request.GET['date'][:10].replace('-',''), "%Y%m%d").date() if self.request.GET else date.today()

		try:
			diaries = paginator.page(page)
		except PageNotAnInteger:
			diaries = paginator.page(1)
		except EmptyPage:
			diaries = paginator.page(paginator.num_pages)
		context['diary_details'] = zip(diaries, detail_links)
		context['add_diary_link'] = reverse_lazy('diary_create')
		context['go_home_link'] = reverse_lazy('home')
		context['entry_date'] = entry_date
		context['form'] = DateSelectorForm()
		return context

@method_decorator(login_required, name='dispatch')
class DiaryDetailView(DetailView):
	model = Diary
	template_name = 'diary/detail.html'
	context_object_name = 'diary'

	def get_object(self, queryset=None):
		obj = super(DiaryDetailView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(DiaryDetailView, self).get_queryset()
		return queryset.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(DiaryDetailView, self).get_context_data(**kwargs)
		diary = context['diary']
		delete_link = reverse_lazy('diary_delete', kwargs={'pk':diary.pk})
		update_link = reverse_lazy('diary_update', kwargs={'pk':diary.pk})
		context['delete_link'] = delete_link
		context['update_link'] = update_link
		context['go_back_link'] = reverse_lazy('diaries_list')
		return context


@method_decorator(login_required, name='dispatch')
class DiaryUpdateView(UpdateView):
	model = Diary
	template_name = 'diary/update.html'
	context_object_name = 'diary'
	fields = ('title', 'content')

	def get_success_url(self):
		return reverse_lazy('diary_detail', kwargs={'pk':self.object.id})

	def get_object(self, queryset=None):
		obj = super(DiaryUpdateView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(DiaryUpdateView, self).get_queryset()
		return queryset.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class DiaryDeleteView(DeleteView):
	model = Diary
	template_name = 'diary/delete.html'
	success_url = reverse_lazy('diaries_list')

	def get_object(self, queryset=None):
		obj = super(DiaryDeleteView, self).get_object(queryset=queryset)
		if obj.user != self.request.user:
			raise Http404()
		return obj

	def get_queryset(self):
		queryset = super(DiaryDeleteView, self).get_queryset()
		return queryset.filter(user=self.request.user)


# api for Diary

@method_decorator(login_required, name='dispatch')
class DiaryList(APIView):

	def get(self, request, format=None):
		diaries = Diary.objects.filter(user=request.user)
		serializer = DiarySerializer(diaries, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = DiarySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class DiaryDetail(APIView):
	def get_object(self, pk):
		try:
			diary = Diary.objects.get(pk=pk)
			if diary.user != self.request.user:
				raise Http404()
			return expense
		except Expense.DoesNotExist:
			raise Http404()

	def get(self, request, pk, format=None):
		diary = self.get_object(pk)
		serializer = DiarySerializer(diary)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		diary = self.get_object(pk)
		serializer = DiarySerializer(Diary, data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		diary = self.get_object(pk)
		diary.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
