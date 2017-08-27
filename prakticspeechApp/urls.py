from django.conf.urls  import url
from prakticspeechApp import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^registerUserVoice/', views.registerUserVoice, name = 'registerUserVoice'),
    url(r'^loginUserByVoice/', views.loginUserByVoice, name = 'loginUserByVoice')
]
