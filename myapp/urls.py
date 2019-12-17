from django.urls import path
from . import views

urlpatterns = [
	path('', views.list, name='list'),
	path('text/', views.rasp, name = 'text'),
	path('download/download_file', views.download_file),
	path('download/', views.download, name = 'download'),

]
