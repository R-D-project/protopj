from django.shortcuts import render
from .models import GoodsTBL
from .models import HighCategoryTBL
# Create your views here.

def post_list(request):
    posts = 'a'
    return render(request,'searchapp/details.html',{'posts':posts})
