from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.ListListView.as_view(), name='lists_list'),
    path('create/', views.ListCreateView.as_view(), name='list_create'),
    path('detail/<int:pk>', views.ListDetailView.as_view(), name='list_detail'),
    path('update/<int:pk>', views.ListUpdateView.as_view(), name='list_update'),
    path('delete/<int:pk>', views.ListDeleteView.as_view(), name='list_delete'),
    path('list_entry_list/<list_id>', views.ListEntryListView.as_view(), name='list_entries_list'),
    path('list_entry_create/<list_id>', views.ListEntryCreateView.as_view(), name='list_entry_create'),
    path('list_entry_detail/<list_id>/<int:pk>', views.ListEntryDetailView.as_view(), name='list_entry_detail'),
    path('list_entry_update/<list_id>/<int:pk>', views.ListEntryUpdateView.as_view(), name='list_entry_update'),
    path('list_entry_delete/<list_id>/<int:pk>', views.ListEntryDeleteView.as_view(), name='list_entry_delete'),

]
