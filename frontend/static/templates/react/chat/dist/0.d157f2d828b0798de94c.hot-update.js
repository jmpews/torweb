webpackHotUpdate(0,{

/***/ 284:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(280);

	var _utils = __webpack_require__(286);

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	var React = __webpack_require__(78);


	var setCurrentUser = function setCurrentUser(id, avatar, name) {
	    _index.store.dispatch({
	        type: _ActionTypes.SET_CURRENT_USER,
	        payload: {
	            id: id,
	            avatar: avatar,
	            name: name
	        }
	    });
	};

	var UserList = function (_React$Component) {
	    _inherits(UserList, _React$Component);

	    function UserList() {
	        _classCallCheck(this, UserList);

	        return _possibleConstructorReturn(this, (UserList.__proto__ || Object.getPrototypeOf(UserList)).apply(this, arguments));
	    }

	    _createClass(UserList, [{
	        key: 'render',
	        value: function render() {
	            var _this = this;
	            var recent_user_list = this.props.recent_user_list;
	            var users = recent_user_list.map(function (user, index) {
	                var other_id = user.id;
	                var other_avatar = '/assets/images/avatar/' + user.avatar;
	                var other_name = user.name;
	                return React.createElement(
	                    'div',
	                    { key: index, className: 'chat-user', 'data-other': other_id, onClick: setCurrentUser(other_id, other_avatar, other_name) },
	                    React.createElement('img', { className: 'chat-user-avatar', src: other_avatar }),
	                    React.createElement(
	                        'span',
	                        { className: 'chat-user-name' },
	                        other_name
	                    )
	                );
	            });

	            return React.createElement(
	                'div',
	                { className: 'user-list' },
	                users
	            );
	        }
	    }]);

	    return UserList;
	}(React.Component);

	module.exports = UserList;
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(setCurrentUser, 'setCurrentUser', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/components/userList.js');

	    __REACT_HOT_LOADER__.register(UserList, 'UserList', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/components/userList.js');
	}();

	;

/***/ },

/***/ 286:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(280);

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
	function handle_receive_message(data) {
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

	    __REACT_HOT_LOADER__.register(handle_receive_message, 'handle_receive_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(start_chat_websocket, 'start_chat_websocket', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');
	}();

	;

/***/ }

})