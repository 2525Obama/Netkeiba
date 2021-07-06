# https://techacademy.jp/magazine/6235#sec4


# リポジトリを新たに作成するコマンド
git init

# Status確認
git status

# ファイルを追加する
git add ***
↓
# localリポジトリにコミットする
git commit -m "add new file"

# リモートリポジトリの情報を追加する
git remote add origin https://github.com//***.git]

# localリポジトリをPushしてリモートリポジトリへ反映する
※masterでうまくいかない場合はmain
git push origin master


# localリポジトリの中身をremoteリポジトリの内容に更新する
※remoteリポジトリにつながっていない場合は以下のコマンドも実行
git remote add origin git@github.com
git pull origin master
