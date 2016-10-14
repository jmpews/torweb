var React = require('react');
var MessageList = require('./messageList.js');
var UserList = require('./userList.js');

    // 发送操作码和数据
function send_socket_message(opt, data) {
    if (data == '')
        data = 'x';
    var message = JSON.stringify({
        'opt': opt,
        'data': data
    });
    chat_websocket.send(message);
}

// 设置当前聊天用户
function set_current_user(user_id) {
    window.sessionStorage.setItem('current_user_id', user_id);
}

// 判断是否为当前用户
function is_current_user(user_id) {
    var curent_user_id = window.sessionStorage.getItem('current_user_id');
    if (curent_user_id) {
        if (curent_user_id == user_id) {
            return true
        }
    }
    return false;
}

// 判断 最近用户列表是否存在
function is_current_user_list(user_id) {
    var recent_user_list = window.sessionStorage.getItem('recent_user_list');
    if (recent_user_list) {
        recent_user_list = JSON.parse(recent_user_list);
    }
    else
        return false;
    var user_id_list = recent_user_list.user_id_list;
    if(user_id_list) {
        if(user_id_list.indexOf(user_id)!= -1)
            return true;
    }
    return false;
}

class ChatContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {}
        };
    }

    componentDidMount() {
        var _this = this;
        $.ajax({});
    }

    start_chat_websocket(url) {
        var wsServer = 'ws://' + url + '/user/chatwebsocket';
        chat_websocket = new WebSocket(wsServer);
        chat_websocket.onopen = function (evt) {
            onOpen(evt)
        };
        chat_websocket.onclose = function (evt) {
            onClose(evt)
        };
        chat_websocket.onmessage = function (evt) {
            onMessage(evt)
        };
        chat_websocket.onerror = function (evt) {
            onError(evt)
        };

        function onOpen(evt) {
            console.log("Connected to WebSocket server.");
            // 请求更新 最近用户列表
            send_socket_message('update_recent_user_list', '')
        }

        function onClose(evt) {
            console.log("Disconnected to WebSocket server.");
        }

        function onMessage(evt) {
            var result = JSON.parse(evt.data);
            console.log('Chat onMessage' + result);
            if (result.errorcode == 0) {
                handle_receive_message(result.data);
            }
        }

        function onError(evt) {
            console.log('Error occured: ' + evt.data);
        }
    }

    render() {
        var _this = this;
        return (
            <div className="chat-container">
                <div className="chat-header">
                    <a href="#blank" className="chat-title">chat title</a>
                    <a href="#blank" className="chat-close">X</a>
                </div>
                <div className="chat-content">
                    <UserList />
                    <MessageList/>
                </div>
                <div className="chat-footer">
                    <form className="form-group row">
                        <textarea className="form-control" cols="2">Write Here.</textarea>
                        <button type="submit" className="btn btn-primary col-sm2">发送</button>
                    </form>
                </div>
            </div>
        );
    }
}

function select(state) {
    return {
        state: state.chat
    }
}

export default connect(select)(AppleBusket);
