webpackHotUpdate(0,{

/***/ 283:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(281);

	var _index2 = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"../actions/index\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

	// 发送操作码和数据
	function send_socket_message(opt, data) {
	    if (data == '') data = 'x';
	    var message = JSON.stringify({
	        'opt': opt,
	        'data': data
	    });
	    chat_websocket.send(message);
	}

	function send_message(text) {
	    send_socket_message('send_message', text);
	}

	// 根据操作码,处理接收到的消息数据
	function handle_receive_messagex(data) {
	    // 最近用户列表
	    if (data.code == 'recent_user_list') {
	        _index.store.dispatch({
	            type: _ActionTypes.RECENT_USER_LIST,
	            payload: data.data
	        });
	    }

	    // 最近消息列表
	    else if (data.code == 'recent_message_list') {
	            _index.store.dispatch({
	                type: _ActionTypes.RECENT_MESSAGE_LIST,
	                payload: data.data
	            });
	        }
	        // 一条消息
	        else if (data.code == 'receive_a_message') {
	                _index.store.dispatch({
	                    type: _ActionTypes.RECEIVE_A_MESSAGE,
	                    payload: data.data
	                });
	            }
	}
	var handle_receive_message = function handle_receive_message(data) {
	    return function (dispatch, getState) {
	        // 最近用户列表
	        if (data.code == 'recent_user_list') {
	            dispatch((0, _index2.updateRecentUserList)(data.data));
	        }

	        // 最近消息列表
	        else if (data.code == 'recent_message_list') {
	                dispatch((0, _index2.updateRecentMessageList)(data.data));
	            }
	            // 一条消息
	            else if (data.code == 'receive_a_message') {
	                    dispatch(receiveAMessage(data.data));
	                }
	    };
	};

	function start_chat_websocket(url) {
	    var wsServer = 'ws://' + url + '/user/chatwebsocket';
	    chat_websocket = new WebSocket(wsServer);
	    chat_websocket.onopen = function (evt) {
	        onOpen(evt);
	    };
	    chat_websocket.onclose = function (evt) {
	        onClose(evt);
	    };
	    chat_websocket.onmessage = function (evt) {
	        onMessage(evt);
	    };
	    chat_websocket.onerror = function (evt) {
	        onError(evt);
	    };

	    function onOpen(evt) {
	        console.log("Connected to WebSocket server.");
	        send_socket_message('update_recent_user_list', '');
	    }

	    function onClose(evt) {
	        console.log("Disconnected");
	    }

	    function onMessage(evt) {
	        var data = JSON.parse(evt.data);
	        console.log(data);
	        if (result.errorcode == 0) {
	            handle_receive_message(data.data);
	        }
	    }

	    function onError(evt) {
	        console.log('Error occured: ' + evt.data);
	    }
	}
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(send_socket_message, 'send_socket_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(send_message, 'send_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(handle_receive_messagex, 'handle_receive_messagex', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(handle_receive_message, 'handle_receive_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(start_chat_websocket, 'start_chat_websocket', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');
	}();

	;

/***/ },

/***/ 286:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.receiveAMessage = exports.updateRecentMessageList = exports.setCurrentUser = exports.updateRecentUserList = undefined;

	var _ActionTypes = __webpack_require__(281);

	var types = _interopRequireWildcard(_ActionTypes);

	var _utils = __webpack_require__(283);

	function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

	var prefix = 'chat/'; /**
	                       * Created by jmpews on 2016/10/14.
	                       */

	var updateRecentUserList = exports.updateRecentUserList = function updateRecentUserList(recent_user_list) {
	    return function (dispatch, getState) {
	        console.log('updateRecentUserList', recent_user_list);
	        dispatch({
	            type: types.RECENT_USER_LIST,
	            payload: recent_user_list
	        });
	    };
	};

	var setCurrentUser = exports.setCurrentUser = function setCurrentUser(id, avatar, name) {
	    return function (dispatch, getState) {
	        dispatch({
	            type: types.SET_CURRENT_USER,
	            payload: {
	                id: id,
	                avatar: avatar,
	                name: name
	            }
	        });

	        (0, _utils.send_socket_message)('update_recent_message', { 'user_id': id });
	    };
	};

	var updateRecentMessageList = exports.updateRecentMessageList = function updateRecentMessageList(recent_message_list) {
	    return function (dispatch, getState) {
	        dispatch({
	            type: types.RECENT_MESSAGE_LIST,
	            payload: recent_message_list
	        });
	    };
	};
	var receiveAMessage = exports.receiveAMessage = function receiveAMessage(message) {
	    return function (dispatch, getState) {
	        dispatch({
	            type: types.RECEIVE_A_MESSAGE,
	            payload: message
	        });
	    };
	};
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(prefix, 'prefix', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/actions/index.js');

	    __REACT_HOT_LOADER__.register(updateRecentUserList, 'updateRecentUserList', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/actions/index.js');

	    __REACT_HOT_LOADER__.register(setCurrentUser, 'setCurrentUser', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/actions/index.js');

	    __REACT_HOT_LOADER__.register(updateRecentMessageList, 'updateRecentMessageList', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/actions/index.js');

	    __REACT_HOT_LOADER__.register(receiveAMessage, 'receiveAMessage', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/actions/index.js');
	}();

	;

/***/ }

})