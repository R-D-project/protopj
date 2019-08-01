'''
searchappアプリのURL設定ファイル
'''
from django.urls import path
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

# 第3引数の name=’index’) はurlの逆引き用です。
# 別viewへのリダイレクトやtemplate内でのリンクに使用します。
urlpatterns = [
    # 'result/'を指定した場合にviewクラス(ResultListView)を起動する。
    path('result/', views.ResultListView.as_view(), name='result'),
    # 'details/'を指定した場合にviewクラス(DetailsListView)を起動する。
    path('details/', views.DetailsListView.as_view(), name='details'),
]
