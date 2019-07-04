from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'
'''
urlpatterns = [
    path('', views.IndexView.as_view(), name='details'),
]
'''