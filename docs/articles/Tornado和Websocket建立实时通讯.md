Title: Tornado和Websocket建立实时通讯
Date: 20156-09-27
Author: jmpews
Category: tornado
Tags: Tornado, Websocket
Slug: tornado-websocket-real-time-chat

## Summary:

需要在web上建立实时通讯的一个Widget, 找了一些Tornado和Websocket结合的方案, 发现都很简单, 然后就结合具体实现了一个方案.

## Feature:

1. 支持通讯记录
2. 支持多人的通讯
3. 支持sessionStorage缓存
4. 界面上显示聊天列表(待)

## Tornado & Websocket 简介

略...

## JS的解决方案

```
// 启动聊天的websocket
function start_chat_websocket(url) {
     var  wsServer = 'ws://' + url + '/user/chatwebsocket';
     chat_websocket = new WebSocket(wsServer);
     chat_websocket.onopen = function (evt) { onOpen(evt) };
     chat_websocket.onclose = function (evt) { onClose(evt) };
     chat_websocket.onmessage = function (evt) { onMessage(evt) };
     chat_websocket.onerror = function (evt) { onError(evt) };

     function onOpen(evt) {
        console.log("Connected to WebSocket server.");
        window.sessionStorage.setItem('current_other', '');
     }

     function onClose(evt) {
        console.log("Disconnected");
     }

     function onMessage(evt) {
         var result = JSON.parse(evt.data);
         console.log(result);
         // 接受发送过来信息
         if(result.errorcode == 0) {
             // data = {'user_id': 2, 'data': ['>', 'test, '2015/09/26']}
             var data = JSON.parse(evt.data).data;
             // 发送者user_id
             var user_id = data.user_id;

            //cache_user_data = {me_avatar: "admin.png", me_name: "admin", other_avatar: "default_doubi.png", other_name: "test", logs: Array[6]}
             // 需要缓存这个数据
            var cache_user_data = window.sessionStorage.getItem(data.user_id);
            if(cache_user_data) {
                // 如果有缓存数据直接从从缓存数据中取
                cache_chat_log(data, chat_init);
            }
            else {
                // 如果不存在缓存数据，重新从服务端拉取
                get_chat_log(user_id, chat_init);
            }
         }
         // 返回发送成功的信息
         else if(result.errorcode == 1) {
             // data = {'me_id': 2, 'data': ['>', 'test, '2015/09/26']}
             var data = JSON.parse(evt.data).data;
             // 发送者user_id
             var user_id = data.user_id;
             // 需要缓存这个数据
             var cache_user_data = window.sessionStorage.getItem(data.user_id);
             if(cache_user_data) {
                // 如果有缓存数据直接从从缓存数据中取
                cache_chat_log(data, chat_init);
             }
             else {
                // 如果不存在缓存数据，重新从服务端拉取
                 get_chat_log(user_id, chat_init);
             }
         }
         else if(result.errorcode == 2){
             $.notify('未在线,等待上线回复.')
         }
         else if(result.errorcode == 3){
         }
         else if(result.errorcode != 0)
            alert(result.txt);

     }
     function onError(evt) {
        console.log('Error occured: ' + evt.data);
     }
}

// 缓存聊天记录
function cache_chat_log(data, callback) {
    // cache_user_data = {me_avatar: "admin.png", me_name: "admin", other_avatar: "default_doubi.png", other_name: "test", logs: Array[6]}
    // 字符串缓存 -> 格式化为json -> 把新的聊天记录push到data.logs -> 重新格式化字符串保存到缓存中
    // 然后把数据json格式化成字符串保存到sessionStorage
     var cache_user_data = window.sessionStorage.getItem(data.user_id);
     cache_user_data = JSON.parse(cache_user_data);
     cache_user_data.logs.push(data.data)
     window.sessionStorage.setItem(data.user_id, JSON.stringify(cache_user_data));
     callback(cache_user_data);
}

// 获取聊天记录
// 如果没有缓存或者没有启用localStorage，那么需要重新从服务器获取聊天记录
function get_chat_log(other_id, callback) {
    $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/useropt',
        data: JSON.stringify({
            'opt': 'realtime-chat',
            'data': {'other': other_id}
        }),
        success: function(result, status) {
            if(result.errorcode == 0) {
                var data = result['data'];
                // data = {me_avatar: "admin.png", me: "admin", other_avatar: "default_doubi.png", other: "test", logs: Array[6]}]
                // 设置最初始的缓存
                window.sessionStorage.setItem(other_id, JSON.stringify(data));
                callback(data);
            }
            else if(result.errorcode == -3) {
                $.notify(result.txt);
                return false;
                }
            else if(result.errorcode != 0) {
                $.notify(result.txt);
                return false;
            }
        }
    });
}

// 把聊天记录格式到组件
function chat_init(data) {
    console.log(data);
    if(!data)
        return;
    $('.chat .chat-header').html('chat 2 ' + data['me']);
    $('.chat .chat-header').attr('other_avatar', data['other_avatar']);
    $('.chat .chat-header').attr('me_avatar', data['me_avatar']);
    var chatlog = data['logs'];
    var chatcontent = $('.chat .chat-content ul');
    $(chatcontent).html('');
    for(var i = 0; i < chatlog.length; i++) {
        if (chatlog[i][0] == "<")
            var s = "<li class='chat-other cl'><img class='avatar' src='/assets/images/avatar/"+data['other_avatar']+"'><div class='chat-text'>"+chatlog[i][1]+"</div></li>";
        else
            var s = "<li class='chat-self cl'><img class='avatar' src='/assets/images/avatar/"+data['me_avatar']+"'><div class='chat-text'>"+chatlog[i][1]+"</div></li>";
        $(chatcontent).append(s)
    }
    $('.chat-container').show();
}
```

## Tornado的解决方案

DB用的mysql, driver用的是peewee.

### 数据模型

```
class ChatLog(BaseModel):
    me = ForeignKeyField(User, related_name='who-send')
    other = ForeignKeyField(User, related_name='send-who')
    content = TextField(verbose_name='chat-content')
    time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_chat_log(me, other):
        '''
        获取双方对话的聊天记录
        :param self:
        :param other:
        :return:
        '''
        result = {'me': '', 'other': '', 'logs': []}
        result['me'] = me.username
        result['other'] = other.username
        result['me_avatar'] = me.avatar
        result['other_avatar'] = other.avatar
        # import pdb;pdb.set_trace()

        # () 注意需要全包
        chatlogs = (ChatLog.select().where(((ChatLog.me == me) & (ChatLog.other == other)) | ((ChatLog.me == other) & (ChatLog.other == me))).order_by(ChatLog.time).limit(10))
        for cl in chatlogs:
            d = '>' if cl.me == me else '<'
            result['logs'].append([d, cl.content, TimeUtil.datetime_delta(cl.time)])
        return result
```

### Websocket处理Handler

处理handler的地方加了一个peewee的hook，在sql处理前建立连接，处理完成后释放连接

```
class WebsocketChatHandler(BaseWebsocketHandler):
    """
    使用websocket的实时聊天

    websocket real-time-chat
    """

    # redis ?
    clients = {}

    def check_origin(self, origin):
        return True

    @ppeewwee
    def open(self, *args, **kwargs):

        user = self.current_user
        if user.username not in WebsocketChatHandler.clients.keys():
            WebsocketChatHandler.clients[user.username] = self

    @ppeewwee
    def on_close(self):
        user = self.current_user

        if user.username in WebsocketChatHandler.clients.keys():
            WebsocketChatHandler.clients.pop(user.username)
        else:
            logger.debug("[{0}] not in Websocket.clients, but close.".format(user.username))

    @staticmethod
    def is_online(username):
        w = WebsocketChatHandler.clients.get(username, False)
        return w

    @ppeewwee
    def on_message(self, message):
        json_data = get_cleaned_json_data_websocket(message, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']
        if opt == 'chat-to':
            user = self.current_user
            # 目标用户
            other_id = data['other']
            other = User.get(User.id == other_id)
            content = data['content']
            cl = ChatLog.create(me=user, other=other, content=content)

            #push to [other]
            other_websocket = WebsocketChatHandler.is_online(other.username)
            if other_websocket:
                # <
                other_websocket.write_message(json_result(0, {'user_id': user.id, 'data': ['<', cl.content, TimeUtil.datetime_delta(cl.time)]}))
                # >
                self.write_message(json_result(1, {'user_id': other.id, 'data': ['>', cl.content, TimeUtil.datetime_delta(cl.time)]}))
            else:
                self.write_message(json_result(2, 'success.'))

        else:
            self.write_message(json_result(-1, 'not support opt.'))
```
