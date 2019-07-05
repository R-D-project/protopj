from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    path('',views.SearchScreen.as_view(),name='search'),
    path('result/<str:pk>/', views.ResultList.as_view(), name='result'),
#    path('',views.details,name='details'),
#    path('details/<str:pk>/',views.details_list,name='details'),
    path('details/<str:pk>/', views.DetailsView.as_view(), name='details'),
]
