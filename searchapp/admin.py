'''
adminページを表示するためのコード
'''

from django.contrib import admin
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL

# Register your models here.

admin.site.register(GoodsTBL)
admin.site.register(CategoryTBL)
admin.site.register(HighCategoryTBL)
