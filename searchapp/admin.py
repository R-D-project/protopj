'''
管理者画面を表示するためのコード
'''
from django.contrib import admin
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL


# 管理者画面に表示するテーブルを定義
admin.site.register(GoodsTBL)
admin.site.register(CategoryTBL)
admin.site.register(HighCategoryTBL)
