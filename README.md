## 目录
* [说明](#1)
* [功能](#2)
* [如何使用](#3)

## <a name="1">说明</a>

这是一个用Django开发的多人博客系统，功能简单，但完全满足公司内部或个人的博客使用需求。支持普通富文本编辑器(tinyMCE)和MarkDown编辑器
由于嫌弃Django后台太难看，也无法满足个人开发时候的想法。于是自主开发了后台，未使用Django自带的admin模块。其中集成了Django的Auth模块，其他部分都重写了
由于本人前端不精，不愿意花费大量时间去写界面。所以博客前台界面参考了[vmaig](http://www.vmaig.com/)开源博客的界面。后台模块的界面参考了Bootstrap的metronic响应式模板
除此之外，还使用了python中著名的PIL图片处理模块来压缩图片，也使用了Django-tagging来处理博文标签
博客将会持续开发新功能，在现有基础上不断完善

## <a name="2">功能</a>

#####已实现：
* 多用户支持。每个用户有自己的后台
* 用户添加修改删除
* 用户头像切换，密码修改等功能
* 博文发布，删除，存为草稿
* 添加博文标签，添加博文到目录
* 编辑器切换（目前支持MarkDown和tinyMCE）
* 博文评论，可进行楼中楼评论
* 博文轮播
* 热门博文统计
* 用户发布博文统计

基本上就是实现了正常博客最基本的，应该有的功能

#####未实现：
* 不能进行目录管理，目前只能通过数据库直接添加目录

原因是个人认为目录应该在博客部署时，一次性添加完毕，在以后的使用中不能修改或者添加新的目录，所以未实现此功能
 
#####将实现：
* 博客编写时，本地自动保存
* 用户动态跟踪，展示用户使用博客的时间线
* 文件上传管理

## <a name="3">如何使用</a>

需要安装的包：
django
django-tagging
pillow(该包为PIL的一个分支，目前pip和easy_install好像都无法下载安装PIL了)
MySQL-python（还有一个数据库驱动，我使用的是MySQL，你也可以使用其他驱动）

安装完成后，打开 zer0Blog/settings，修改其中的数据库配置。配置如下：

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'zer0Blog',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        }
    }

若使用MySQL，则需要修改 `USER` ,`PASSWORD`,`HOST` 和你想使用的数据库名 `NAME`。若使用其他数据库，还需要修改 `ENGINE'。熟悉 Django 的都知道怎么做，就不细说了

然后就是在项目根目录下输入 `python manager.py makemigrations` ，再输入 `python manager.py migrate` 生成数据库表。然后使用 `python manager.py runserver` 启动数据库即可。

一个要点:`管理员账户必须使用 python manager.py createsuperuser 命令来创建`

若要正式部署使用，建议使用 nginx+uwsgi 部署，可参考[Nginx+uWSGI安装与配置](http://mdba.cn/?p=109)
