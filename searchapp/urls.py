'''
アプリURLの設定を行っている。

'''
from django.urls import path  # path機能インポート(デフォルト)
from . import views  # searchapp(自分)からviews.pyインポート


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

# 第3引数の name=’index’) はurlの逆引き用です。
# 別viewへのリダイレクトやtemplate内でのリンクに使用します。
urlpatterns = [
    # URLの指定なしの場合、views.pyのIndexViewの処理を動かす
    path('', views.IndexView.as_view(), name='index'),
    # URLに'result/'を指定している場合、views.pyのResultListの処理を動かす
    path('result/', views.ResultList.as_view(), name='result'),
    # 'details/'を指定した場合にviewクラス(DetailsListView)を起動する。
    path('details/', views.DetailsListView.as_view(), name='details'),
    # URLに'login/'を指定している場合、views.pyのLoginの処理を動かす
    path('login/', views.Login.as_view(), name='login'),
    # URLに'logout/'を指定している場合、views.pyのLogoutの処理を動かす
    path('logout/', views.Logout.as_view(), name='logout'),
]
