'''
searchappアプリのURL設定ファイル
'''
from django.urls import path
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    # 第3引数の name=’index’) はurlの逆引き用です。別viewへのリダイレクトやtemplate内でのリンクに使用します。
    path('', views.ResultListView.as_view(), name='result'),
    path('details/', views.DetailsListView.as_view(), name='details'),
]
