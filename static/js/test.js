// TODO(勝俣)selectChangeは使用しないため、UTテスト後に削除予定
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

	// TODO(勝俣)UTテスト後に削除予定
	//sizef = document.selform.size;
	//sizeindex = sizef.selectedIndex;
	//colorf = document.selform.color;
	//colorindex = colorf.selectedIndex;

	//form名がselformをsubmit
	document.selform.submit();

}