from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.IncomeListView.as_view(), name='incomes_list'),
    path('create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('detail/<int:pk>', views.IncomeDetailView.as_view(), name='income_detail'),
    path('update/<int:pk>', views.IncomeUpdateView.as_view(), name='income_update'),
    path('delete/<int:pk>', views.IncomeDeleteView.as_view(), name='income_delete')
]
