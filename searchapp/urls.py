from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    path('',views.post_list,name='post_list'),
#    path('', views.IndexView.as_view(), name='details'),
]
