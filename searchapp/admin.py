from django.contrib import admin
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL

# Register your models here.
'''
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goodsid','categoryname','sizename','colorname','goodsname')
    def categoryname(self,obj):
        return obj.categoryid.categoryname
    categoryname.short_description = 'categoryname'
'''

admin.site.register(GoodsTBL)
admin.site.register(CategoryTBL)
admin.site.register(HighCategoryTBL)