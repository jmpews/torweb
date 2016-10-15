webpackHotUpdate(0,{

/***/ 248:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});

	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _chat = __webpack_require__(249);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

	// import { connect } from 'react-redux'

	var MessageList = __webpack_require__(250);
	var UserList = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"../components/userList.js\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

	var ChatContainer = function (_React$Component) {
	    _inherits(ChatContainer, _React$Component);

	    function ChatContainer(props) {
	        _classCallCheck(this, ChatContainer);

	        var _this2 = _possibleConstructorReturn(this, (ChatContainer.__proto__ || Object.getPrototypeOf(ChatContainer)).call(this, props));

	        _this2.state = {
	            recent_message: _chat.recent_message,
	            recent_users: _chat.recent_users,
	            current_user: _chat.current_user
	        };
	        return _this2;
	    }

	    _createClass(ChatContainer, [{
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            var _this = this;
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _this = this;
	            return _react2.default.createElement(
	                'div',
	                { className: 'chat' },
	                _react2.default.createElement(
	                    'div',
	                    { className: 'chat-header' },
	                    _react2.default.createElement(
	                        'a',
	                        { href: '#blank', className: 'chat-title' },
	                        'chat title'
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
	                    _react2.default.createElement(UserList, { recent_user_list: this.state.recent_users })
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

	// function select(state) {
	//     return {
	//         state: state.chat
	//     }
	// }

	// export default connect(select)(ChatContainer);


	var _default = ChatContainer;
	exports.default = _default;
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(ChatContainer, 'ChatContainer', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');

	    __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/containers/chatContainer.js');
	}();

	;

/***/ }

})