from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db.models import Q
from .models import GoodsTBL
from .models import HighCategoryTBL
from django.views.generic.base import TemplateView


# Create your views here.

class IndexView(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/post_list.html'

    # 呼び出された（オーバーライドされたメソッド）
    def get_queryset(self):
    # DBから検索条件に一致したデータを取得

        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
        #if 'form_value' in self.request.session:
            #form_value = self.request.session['form_value']
            #title = form_value[0]
            #category = form_value[1]
            #price = form_value[2]

            #Qオブジェクトを各変数にインスタンス化
            #condition_title = Q()
            #condition_category = Q()
            #condition_price = Q()

            # クエリを発行
            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
            #if len(title) != 0 and title[0]:
            #    condition_title = Q(title__contains = title)
            #if len(category) != 0 and category[0]:
            #    condition_category = Q(category__contains = category)
            #if len(price) != 0 and price[0]:
            #    condition_price = Q(price__contains = price)

            # 定義されたクエリを発行し、データをobject_listへ格納する。
            return GoodsTBL.objects.select_related().all()

#        else:
#            return GoodsTBL.objects.none() # 何も返さない
class DetailsView(TemplateView):
    template_name = 'searchapp/details.html'

    def display(request):
        if request.POST:
            pass

    def details_list(request):
        #posts = get_object_or_404(Post, pk=pk)
        posts = pk
        return render(request,'searchapp/details.html',{'posts':posts})
