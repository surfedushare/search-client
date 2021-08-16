from django.urls import path

from core import views


app_name = 'core'
urlpatterns = public_api_patterns = [
    path('dataset/<int:pk>/documents/', views.DatasetDocumentsView.as_view(), name="dataset-documents"),
    path('dataset/<int:pk>/', views.DatasetDetailView.as_view(), name="dataset-detail"),
    path('dataset/', views.DatasetListView.as_view(), name="datasets"),
    path('extension/<str:pk>/', views.ExtensionDetailView.as_view(), name="extension-detail"),
    path('extension/', views.ExtensionListView.as_view(), name="extensions"),
]
