from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    #第3引数の name=’index’) はurlの逆引き用です。別viewへのリダイレクトやtemplate内でのリンクに使用します。

    #path('',views.SearchScreen.as_view(),name='search'),
    path('', views.details_ListView.as_view(), name='details'),
#    path('result/<str:srh>/', views.ResultList.as_view(), name='result'),
#    path('',views.details,name='details'),
#    path('details/<str:pk>/',views.details_list,name='details'),
#    path('details/<str:id>/', views.Details_detailView.as_view(), name='details'),

]
