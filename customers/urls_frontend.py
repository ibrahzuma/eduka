from django.urls import path
from .views_frontend import ClientListView, ClientCreateView, ClientImportView, ClientUpdateView, ClientTemplateDownloadView

urlpatterns = [
    path('list/', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('import/', ClientImportView.as_view(), name='client_import'),
    path('import/template/', ClientTemplateDownloadView.as_view(), name='client_import_template'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
]
