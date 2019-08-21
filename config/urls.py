
"""config URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# アドミン(管理者)機能のインストール
from django.contrib import admin
# include機能(includeに含まれるURLに遷移する)のインストール
from django.urls import include
# path機能(文字列、url、逆引きの名前を指定して1まとまりとする)のインストール
from django.urls import path

from .settings import local


urlpatterns = [
    # URLに'admin/'が指定されている場合、管理サイト(admin.site.urls)を参照する
    path('admin/', admin.site.urls),
    # URLの指定なしの場合、searchapp内のurls.pyに指定されているURLの処理に移動する
    path('', include('searchapp.urls')),
]


if local.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
