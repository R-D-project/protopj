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

function selChange(){
	//サイズと色が選択されているかを判定する(if文追加)
	document.selectform.submit();
	sizef = document.selform.size;
	sizeindex = sizef.selectedIndex;
	colorf = document.selform.color;
	colorindex = colorf.selectedIndex;
	if(sizef.options[sizeindex].value == "0" && colorf.options[colorindex].value == "1"){
		document.selform.submit();
	}
}