'''
アプリURLの設定を行っている。

'''
from django.urls import path  # path機能インポート(デフォルト)
from . import views  # accounts(自分)からviews.pyインポート


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'accounts'

# 第3引数の name=’index’) はurlの逆引き用です。
# 別viewへのリダイレクトやtemplate内でのリンクに使用します。
urlpatterns = [
    # URLに'login/'を指定している場合、views.pyのLoginの処理を動かす
    path('login/', views.Login.as_view(), name='login'),
    # URLに'logout/'を指定している場合、views.pyのLogoutの処理を動かす
    path('logout/', views.Logout.as_view(), name='logout'),
]
