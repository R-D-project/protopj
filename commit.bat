:インデックスへ上げて、コミットしてリモートにpushするところまで
:第一引数　日単位のcommit数
:第二引数　修正中のファイル名
:第三引数　修正中のソースコード番号
:第四引数　修正中のソースコード(1行)
@set date0=%date:~0,4%%date:~5,2%%date:~8,2%

git status
git add --all .
git status
git commit -m "%date0%_commit_%1" -m "%2_%3_%~4"

:pushするか判定する。
@set /P ANSWER="pushを実行します。よろしいですか（y/n)?"

@if /i {%ANSWER%}=={y} (goto :yes)
@if /i {%ANSWER%}=={yes} (goto :yes)

@EXIT

:yes
git push origin master