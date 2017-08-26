from django.conf.urls  import url
from prakticspeechApp import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^storeFileData/', views.storeFileData, name = 'storeFileData'),
]
