function selectChange(){
	//サイズと色が選択されているかを判定する(if文追加)
	sizef = document.selectform.sizeselect;
	sizeindex = sizef.selectedIndex;
	colorf = document.selectform.colorselect;
	colorindex = colorf.selectedIndex;
	if(sizef.options[sizeindex].value != "-" && colorf.options[colorindex].value != "-"){
		document.selectform.submit();
	}
}
function colorChange(){

	document.selectfm.submit();
	//documentとは：webページを構成するhtml要素
	//document.getElementById：指定したID属性を持つhtml属性を取得する。

	//zaiko_eleにhtml側で定義した"zaiko"idを定義する。
	//var zaiko_ele = document.getElementById('zaiko');
	//color_eleにhtml側で定義したフォーム(colorfm)のプルダウン(colorselect)を定義する。
	//var color_ele = document.colorfm.colorselect;
	//color_indexにプルダウン(color_ele)で選択されている項目(selectedIndex)を定義する。
	//var color_index = color_ele.selectedIndex;

	//zaiko_ele(今回は"zaiko"id)にプルダウン(color_ele)のオプションで現在定義(color_index)されている値(value)を出力する。
	//zaiko_ele.innerHTML = color_ele.options[color_index].value;

	//変数の状態お試し用(ポップアップ表示)
	//alert(a)
	//("{{ goodsform.goodsid }}")


}
function sizeChange(){

	document.sizeform.submit();
	//zaiko_eleにhtml側で定義した"zaiko"idを定義する。
	//var zaiko_ele = document.getElementById('zaiko');
	//size_eleにhtml側で定義したフォーム(sizefm)のプルダウン(sizeselect)を定義する。
	//var size_ele = document.sizefm.sizeselect;
	//size_indexにプルダウン(size_ele)で選択されている項目(selectedIndex)を定義する。
	//var size_index = size_ele.selectedIndex;

	//zaiko_ele(今回は"zaiko"id)にプルダウン(size_ele)のオプションで現在定義(size_index)されている値(value)を出力する。
	//zaiko_ele.innerHTML = size_ele.options[size_index].value;
}

