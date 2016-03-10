# Tornado项目模板

## Web框架
Tornado

## 设计特点:

### DB使用:
Mongo做session存储、服务器stats(url访问统计)

Reis做访问频率限制以及cache缓存(其实可以在nginx进行控制)

Mysql做Data—DB

### LOG及异常处理
重写`requesthandler`的`write_error`，返回500.html

添加`default_handler_class`，处理404，并做好LOG

添加Logger

### 参数安全处理
对参数进行clean

### Mongo设计 

#### 用户Session
`{ "_id" : "encrypt_id", "data" : { "key" : "value" } }`

Ex: `{ "_id" : "Km9hAb58ePjV9NdJtBR0lxNMmSPfe6e3Kmi43n6gsDMp1GTWet8wHS3mYjcX6g", "data" : { "openid" : "test" } }`

### Redis设计
#### 用户访问频率限制
`'ratelimit:ip':count`

Ex: `'ratelimit:127.0.0.1':5` & `expire(5)`

### 添加了几个封装好的handler

`Adv__BaseRequestHandler` session和url访问记录handler

`Rate_BaseRequestHandler` 访问频率处理handler

## 使用&测试

根据需要注释`handlers/index.py`的相应模块进行测试
