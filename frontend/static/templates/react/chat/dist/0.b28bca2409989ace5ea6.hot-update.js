webpackHotUpdate(0,{

/***/ 77:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.store = undefined;

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _reactDom = __webpack_require__(110);

	var _redux = __webpack_require__(248);

	var _reactRedux = __webpack_require__(262);

	var _reduxLogger = __webpack_require__(271);

	var _reduxLogger2 = _interopRequireDefault(_reduxLogger);

	var _reduxThunk = __webpack_require__(277);

	var _reduxThunk2 = _interopRequireDefault(_reduxThunk);

	var _index = __webpack_require__(278);

	var _index2 = _interopRequireDefault(_index);

	var _chatContainer = __webpack_require__(282);

	var _chatContainer2 = _interopRequireDefault(_chatContainer);

	var _ActionTypes = __webpack_require__(281);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	var middleware = [_reduxThunk2.default];

	var store = exports.store = (0, _redux.createStore)(_index2.default, _redux.applyMiddleware.apply(undefined, middleware));

	debugger;

	//test---
	store.dispatch({
	  type: _ActionTypes.RECENT_MESSAGE_LIST,
	  payload: {
	    id: 2,
	    avatar: '/jmpews.png',
	    name: 'jmpews',
	    msg: [['>', 'send_disptch'], ['<', 'recv_dispath']]
	  }
	});

	//---

	(0, _reactDom.render)(_react2.default.createElement(
	  _reactRedux.Provider,
	  { store: store },
	  _react2.default.createElement(_chatContainer2.default, null)
	), document.getElementById('chat-container'));
	;

	var _temp = function () {
	  if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	    return;
	  }

	  __REACT_HOT_LOADER__.register(middleware, 'middleware', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/index.js');

	  __REACT_HOT_LOADER__.register(store, 'store', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/index.js');
	}();

	;

/***/ },

/***/ 282:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _reactRedux = __webpack_require__(262);

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(281);

	var _utils = __webpack_require__(283);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	var MessageList = __webpack_require__(284);
	var UserList = __webpack_require__(285);

	var ChatContainer = function (_React$Component) {
	    _inherits(ChatContainer, _React$Component);

	    function ChatContainer(props) {
	        _classCallCheck(this, ChatContainer);

	        // this.state = {
	        //     recent_message: recent_message,
	        //     recent_users: recent_users,
	        //     current_user: current_user
	        // };
	        var _this2 = _possibleConstructorReturn(this, (ChatContainer.__proto__ || Object.getPrototypeOf(ChatContainer)).call(this, props));

	        _this2.state = _this2.props;
	        console.log('ChatContainer-constructor.');
	        return _this2;
	    }

	    _createClass(ChatContainer, [{
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            var _this = this;
	            // start_chat_websocket('127.0.0.1:9000');
	            // send_socket_message('update_recent_user', '')
	            // debugger;
	            // let { state, dispatch } = this.props;
	            console.log('recent_user_list');
	            _index.store.dispatch({
	                type: _ActionTypes.RECENT_USER_LIST,
	                payload: [{
	                    id: 1,
	                    avatar: '/admin.png',
	                    name: 'admin'
	                }, {
	                    id: 1,
	                    avatar: '/admin.png',
	                    name: 'admin'
	                }]
	            });
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _props = this.props;
	            var state = _props.state;
	            var dispatch = _props.dispatch;

	            var _this = this;
	            var current_user = state.current_user;
	            var chat_title = '';
	            if (current_user.id == -1) {
	                chat_title = 'real-time-chat';
	            } else {
	                chat_title = 'chat 2' + current_user.name;
	            }
	            return _react2.default.createElement(
	                'div',
	                { className: 'chat' },
	                _react2.default.createElement(
	                    'div',
	                    { className: 'chat-header' },
	                    _react2.default.createElement(
	                        'a',
	                        { href: '#blank', className: 'chat-title' },
	                        chat_title
	                    ),
	                    _react2.default.createElement(
	                        'a',
	                        { href: '#blank', className: 'chat-close' },
	                        'X'
	                    )
	                ),
	                _react2.default.createElement(
	                    'div',
	                    { className: 'chat-content' },
	                    _react2.default.createElement(UserList, { recent_user_list: state.recent_user_list, actions: { set: set } }),
	                    _react2.default.createElement(MessageList, { recent_message_list: state.recent_message_list })
	                ),
	                _react2.default.createElement(
	                    'div',
	                    { className: 'chat-footer' },
	                    _react2.default.createElement(
	                        'form',
	                        { className: 'form-group row' },
	                        _react2.default.createElement(
	                            'textarea',
	                            { className: 'form-control', cols: '2' },
	                            'Write Here.'
	                        ),
	                        _react2.default.createElement(
	                            'button',
	                            { type: 'submit', className: 'btn btn-primary col-sm2' },
	                            '\u53D1\u9001'
	                        )
	                    )
	                )
	            );
	        }
	    }]);

	    return ChatContainer;
	}(_react2.default.Component);

	// 从总的store树分离出我们需要的state


	function select(state) {
	    console.log('chatContainer-select:', state);
	    return {
	        state: state.chat
	    };
	}

	var _default = (0, _reactRedux.connect)(select)(ChatContainer);

	exports.default = _default;
	// export default ChatContainer;

	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(ChatContainer, 'ChatContainer', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(select, 'select', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');
	}();

	;

/***/ },

/***/ 283:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(281);

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

/***/ },

/***/ 284:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	var React = __webpack_require__(78);

	var MessageList = function (_React$Component) {
	    _inherits(MessageList, _React$Component);

	    function MessageList() {
	        _classCallCheck(this, MessageList);

	        return _possibleConstructorReturn(this, (MessageList.__proto__ || Object.getPrototypeOf(MessageList)).apply(this, arguments));
	    }

	    _createClass(MessageList, [{
	        key: 'render',
	        value: function render() {
	            var _this = this;
	            var recent_message = this.props.recent_message_list;
	            var message_list = recent_message.msg;
	            var messages = message_list.map(function (message, index) {
	                var message_type = '';
	                var img_src = '';
	                if (message[0] == '<') {
	                    message_type = 'chat-other cl';
	                    img_src = '/assets/images/avatar/' + recent_message.avatar;
	                } else {
	                    message_type = 'chat-self cl';
	                    img_src = '/assets/images/avatar/' + recent_message.avatar;
	                }

	                return React.createElement(
	                    'li',
	                    { key: index, className: message_type },
	                    React.createElement('img', { className: 'avatar', src: img_src }),
	                    React.createElement(
	                        'div',
	                        { className: 'chat-text' },
	                        message[1]
	                    )
	                );
	            });

	            return React.createElement(
	                'div',
	                { className: 'message-list' },
	                React.createElement(
	                    'ul',
	                    { id: 'messageList' },
	                    messages
	                )
	            );
	        }
	    }]);

	    return MessageList;
	}(React.Component);

	module.exports = MessageList;
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(MessageList, 'MessageList', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/components/messageList.js');
	}();

	;

/***/ },

/***/ 285:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	var _index = __webpack_require__(77);

	var _ActionTypes = __webpack_require__(281);

	var _utils = __webpack_require__(283);

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	var React = __webpack_require__(78);


	var setCurrentUser = function setCurrentUser(id, avatar, name) {
	    debugger;
	    _index.store.dispatch({
	        type: _ActionTypes.SET_CURRENT_USER,
	        payload: {
	            id: id,
	            avatar: avatar,
	            name: name
	        }
	    });

	    (0, _utils.send_socket_message)('update_recent_message', { 'user_id': id });
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
	            var users = null;
	            users = recent_user_list.map(function (user, index) {
	                var other_id = user.id;
	                var other_avatar = '/assets/images/avatar/' + user.avatar;
	                var other_name = user.name;
	                return React.createElement(
	                    'div',
	                    { key: index, className: 'chat-user', 'data-other': other_id,
	                        onClick: function onClick() {
	                            return setCurrentUser(other_id, other_avatar, other_name);
	                        } },
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

/***/ }

})