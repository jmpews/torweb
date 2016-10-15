webpackHotUpdate(0,{

/***/ 77:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _reactDom = __webpack_require__(110);

	var _reactRedux = __webpack_require__(248);

	var _chatContainer = __webpack_require__(271);

	var _chatContainer2 = _interopRequireDefault(_chatContainer);

	var _globalStore = __webpack_require__(275);

	var _globalStore2 = _interopRequireDefault(_globalStore);

	var _utils = __webpack_require__(274);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	//---
	(0, _utils.start_chat_websocket)('127.0.0.1:9000');

	(0, _reactDom.render)(_react2.default.createElement(
	  _reactRedux.Provider,
	  { store: _globalStore2.default },
	  _react2.default.createElement(_chatContainer2.default, null)
	), document.getElementById('chat-container'));
	;

	var _temp = function () {
	  if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	    return;
	  }
	}();

	;

/***/ },

/***/ 271:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _redux = __webpack_require__(255);

	var _reactRedux = __webpack_require__(248);

	var _index = __webpack_require__(272);

	var _utils = __webpack_require__(274);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	var MessageList = __webpack_require__(280);
	var UserList = __webpack_require__(281);

	var ChatContainer = function (_React$Component) {
	    _inherits(ChatContainer, _React$Component);

	    function ChatContainer(props) {
	        _classCallCheck(this, ChatContainer);

	        var _this2 = _possibleConstructorReturn(this, (ChatContainer.__proto__ || Object.getPrototypeOf(ChatContainer)).call(this, props));

	        _this2.state = _this2.props;
	        console.log('ChatContainer-constructor.');
	        return _this2;
	    }

	    _createClass(ChatContainer, [{
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            (0, _utils.start_chat_websocket)('127.0.0.1:9000');
	        }
	    }, {
	        key: 'componentWillMount',
	        value: function componentWillMount() {
	            // console.log('willMount:',this.props);
	            // let { state, dispatch } = this.props;
	            // var rm = [
	            //     {
	            //         id: 1,
	            //         avatar: '/admin.png',
	            //         name: 'admin'
	            //     },
	            //     {
	            //         id: 1,
	            //         avatar: '/admin.png',
	            //         name: 'admin'
	            //     }
	            // ];
	            // dispatch(updateRecentUserList(rm));
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _props = this.props;
	            var state = _props.state;
	            var dispatch = _props.dispatch;
	            var setCurrentUser = _props.setCurrentUser;

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
	                    _react2.default.createElement(UserList, { recent_user_list: state.recent_user_list, setCurrentUser: setCurrentUser }),
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
	    return {
	        state: state.chat
	    };
	}

	// 注入actions
	function mapDispatchToProps(dispatch) {
	    return {
	        // updateRecentUserList: bindActionCreators(updateRecentUserList, dispatch),
	        // updateRecentMessageList: bindActionCreators(updateRecentMessageList, dispatch),
	        setCurrentUser: (0, _redux.bindActionCreators)(_index.setCurrentUser, dispatch)
	    };
	}

	var _default = (0, _reactRedux.connect)(select, mapDispatchToProps)(ChatContainer);

	exports.default = _default;
	// export default ChatContainer;

	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(ChatContainer, 'ChatContainer', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(select, 'select', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(mapDispatchToProps, 'mapDispatchToProps', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');
	}();

	;

/***/ },

/***/ 272:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.receiveAMessage = exports.updateRecentMessageList = exports.setCurrentUser = exports.updateRecentUserList = undefined;

	var _ActionTypes = __webpack_require__(273);

	var types = _interopRequireWildcard(_ActionTypes);

	var _utils = __webpack_require__(274);

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

/***/ },

/***/ 274:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.handle_receive_message = undefined;
	exports.start_chat_websocket = start_chat_websocket;

	var _globalStore = __webpack_require__(275);

	var _ActionTypes = __webpack_require__(273);

	var _index = __webpack_require__(272);

	var chat_websocket = '';

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
	        _globalStore.store.dispatch({
	            type: _ActionTypes.RECENT_USER_LIST,
	            payload: data.data
	        });
	    }

	    // 最近消息列表
	    else if (data.code == 'recent_message_list') {
	            _globalStore.store.dispatch({
	                type: _ActionTypes.RECENT_MESSAGE_LIST,
	                payload: data.data
	            });
	        }
	        // 一条消息
	        else if (data.code == 'receive_a_message') {
	                _globalStore.store.dispatch({
	                    type: _ActionTypes.RECEIVE_A_MESSAGE,
	                    payload: data.data
	                });
	            }
	}
	var handle_receive_message = exports.handle_receive_message = function handle_receive_message(data) {
	    return function (dispatch, getState) {
	        // 最近用户列表
	        if (data.code == 'recent_user_list') {
	            dispatch((0, _index.updateRecentUserList)(data.data));
	        }

	        // 最近消息列表
	        else if (data.code == 'recent_message_list') {
	                dispatch((0, _index.updateRecentMessageList)(data.data));
	            }
	            // 一条消息
	            else if (data.code == 'receive_a_message') {
	                    dispatch(receiveAMessage(data.data));
	                }
	    };
	};

	function start_chat_websocket(url) {
	    var wsServer = 'ws://' + url + '/user/chatwebsocket';
	    var chat_websocket = new WebSocket(wsServer);
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
	            _globalStore.store.dispatch(handle_receive_message(data.data));
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

	    __REACT_HOT_LOADER__.register(chat_websocket, 'chat_websocket', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(send_socket_message, 'send_socket_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(send_message, 'send_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(handle_receive_messagex, 'handle_receive_messagex', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(handle_receive_message, 'handle_receive_message', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');

	    __REACT_HOT_LOADER__.register(start_chat_websocket, 'start_chat_websocket', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/utils.js');
	}();

	;

/***/ }

})