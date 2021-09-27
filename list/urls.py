from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.ListListView.as_view(), name='lists_list'),
    path('create/', views.ListCreateView.as_view(), name='list_create'),
    path('detail/<int:pk>', views.ListDetailView.as_view(), name='list_detail'),
    path('update/<int:pk>', views.ListUpdateView.as_view(), name='list_update'),
    path('delete/<int:pk>', views.ListDeleteView.as_view(), name='list_delete')
]
