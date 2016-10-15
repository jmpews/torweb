import { store } from './globalStore'

import {
    CHECK_SEND,
    RECENT_MESSAGE_LIST,
    RECENT_USER_LIST,
    RECEIVE_A_MESSAGE
} from './constants/ActionTypes'

import {
    updateRecentUserList,
    updateRecentMessageList,
    setCurrentUser
} from './actions/index'

let chat_websocket = null;

// 发送操作码和数据
export function send_socket_message(opt, data) {
    if (data == '')
        data = 'x';
    var message = JSON.stringify({
        'opt': opt,
        'data': data
    });
    chat_websocket.send(message);
}

function send_message(text) {
    send_socket_message('send_message', text)
}


// 根据操作码,处理接收到的消息数据
function handle_receive_messagex(data) {
    // 最近用户列表
    if (data.code == 'recent_user_list') {
        store.dispatch({
            type: RECENT_USER_LIST,
            payload: data.data
        })
    }

    // 最近消息列表
    else if (data.code == 'recent_message_list') {
        store.dispatch({
            type: RECENT_MESSAGE_LIST,
            payload: data.data
        })
    }
    // 一条消息
    else if (data.code == 'receive_a_message') {
        store.dispatch({
            type: RECEIVE_A_MESSAGE,
            payload: data.data
        })
    }
}
export const handle_receive_message = (data) => (dispatch, getState) => {
    // 最近用户列表
    if (data.code == 'recent_user_list') {
        dispatch(updateRecentUserList(data.data));
    }

    // 最近消息列表
    else if (data.code == 'recent_message_list') {
        dispatch(updateRecentMessageList(data.data));
    }
    // 一条消息
    else if (data.code == 'receive_a_message') {
        dispatch(receiveAMessage(data.data));
    }
}

export function start_chat_websocket(url) {
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
        send_socket_message('update_recent_user_list', '')
    }

    function onClose(evt) {
        console.log("Disconnected");
    }

    function onMessage(evt) {
        var data = JSON.parse(evt.data);
        console.log(data);
        if (data.errorcode == 0) {
            store.dispatch(handle_receive_message(data.data));
        }
    }

    function onError(evt) {
        console.log('Error occured: ' + evt.data);
    }
}


