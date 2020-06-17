Git global setup
git config --global user.name "张惠棣"
git config --global user.email "1412779356@qq.com"

Create a new repository
git clone http://git-meiduo.itheima.net/sh35_zhd/hmtopnews_zhd.git
cd hmtopnews_zhd
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

Push an existing folder
cd existing_folder
git init
git remote add origin http://git-meiduo.itheima.net/sh35_zhd/hmtopnews_zhd.git
git add .
git commit -m "Initial commit"
git push -u origin master

Push an existing Git repository
cd existing_repo
git remote rename origin old-origin
git remote add origin http://git-meiduo.itheima.net/sh35_zhd/hmtopnews_zhd.git
git push -u origin --all
git push -u origin --tags