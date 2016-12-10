## torweb

[![Build Status](https://travis-ci.org/jmpews/torweb.svg?branch=master)](https://travis-ci.org/jmpews/torweb)

基于tornado并且有很多trick用法的社区.

---

## 设计到的功能和模块:
### 前端部分

* 标准化的前端构建流程(gulp+bower)
* 基于react的实时通讯解决方案
* 提供社区类型、展示类型、Blog类型的样式
* 注释详细的scss(部分组件样式引用bootstrap-v4)
* emoji支持
* 采用medium实现用户评论
* TinyMCE的富文本(加了一个支持粘贴上传的插件)
* 主题切换(通过DB和cookie两种方式以保证快速切换)

### 后端部分

* 结构化项目组织
* 很多trick(缓存、异步...)
* 很多utils(时间友好化显示、安全参数获取...)
* 很多decorators(线程异步、peewee的连接释放、login_required)
* 社区功能
* 官方(个人)功能(PS: 可以将md直接导入数据库)
* websocket实现的多用户及时通讯
* 主题切换(通过DB和cookie两种方式以保证快速切换)

---

## 解决方案

把在写torweb遇到的问题，写成解决方案.

[头像裁剪上传解决方案.md](docs/solutions/头像裁剪上传解决方案.md)

[基于react实时通讯解决方案](docs/solutions/react-redux-websocket-chat.md)

---

## 安装&使用

完整安装过程 [docs/full-install.md](docs/full-install.md) (基本不会出错)

```
# py3环境
source ~/virtualenv/python3.5.2/bin/active
git pull https://github.com/jmpews/torweb.git
# 依赖包
pip install -r requirements.txt
# 修改配置文件
vim settings/develoment.py
# 导入测试数据
python tests/test_mysql.py
# 启动服务
python app.py
```

## 组织架构

```
λ : tree -I '*.pyc|__*__|node_modules|bower_components|articles|solutions' -L 3
.
├── LICENSE.md
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── api.py
│   │   └── urls.py
│   ├── blog
│   │   ├── blog.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── cache.py
│   ├── dashboard
│   │   ├── dashboard.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── index
│   │   ├── index.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── post
│   │   ├── post.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── recommend
│   │   ├── recommend.py
│   │   └── urls.py
│   ├── sxuhelp
│   ├── urls.py
│   ├── user
│   │   ├── urls.py
│   │   └── user.py
│   └── utils
│       ├── urls.py
│       └── utils.py
├── app.py
├── configs
│   └── nginx
│       └── tornado.conf
├── custor
│   ├── __init__.py
│   ├── auth.py
│   ├── captcha
│   │   ├── __init__.py
│   │   ├── fonts
│   │   └── image.py
│   ├── decorators.py
│   ├── errors.py
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── basehandler.py
│   │   └── otherhandler.py
│   ├── logger.py
│   ├── uimethods.py
│   └── utils.py
├── db
│   ├── __init__.py
│   ├── mongo_db
│   │   ├── __init__.py
│   │   └── session.py
│   ├── mysql_model
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   ├── common.py
│   │   ├── mysql_db_init.py
│   │   ├── post.py
│   │   └── user.py
│   ├── redis_db
│   │   ├── __init__.py
│   │   └── utils.py
│   └── torweb.sql
├── docs
│   ├── full-install.md
│   └── todo.md
├── frontend
│   ├── bower.json
│   ├── gulpfile.js
│   ├── package.json
│   ├── src
│   │   ├── images
│   │   ├── lib
│   │   ├── scripts
│   │   └── styles
│   ├── static
│   │   ├── assets
│   │   ├── blog
│   │   └── lib
│   └── templates
│       ├── base.html
│       ├── blog
│       ├── dashboard
│       ├── index
│       ├── post
│       ├── react
│       ├── recommend
│       ├── static
│       └── user
├── requirements.txt
├── settings
│   ├── __init__.py
│   ├── common.py
│   ├── config.py
│   ├── development.py
│   ├── language.py
│   └── production.py
├── tags
└── tests
    ├── test_blog_load_from_md.py
    ├── test_captcha.py
    ├── test_gen_couroutine.py
    ├── test_greenlet.py
    ├── test_mysql.py
    └── test_thread_future.py
```
