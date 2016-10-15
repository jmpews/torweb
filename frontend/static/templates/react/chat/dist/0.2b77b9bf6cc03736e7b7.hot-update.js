webpackHotUpdate(0,{

/***/ 250:
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
	            var recent_message = this.props.recent_message;
	            var message_list = recent_message.msg;
	            var messages = message_list.map(function (message, index) {
	                var message_type = '';
	                var img_src = '';
	                if (message[0] == '<') {
	                    message_type = 'chat-other cl';
	                    img_src = '/assets/images/avatar/' + recent_message.avatar;
	                } else {
	                    message_type = 'chat-self cl';
	                    img_src = '/assets/images/avatar/' + _this.props.other_avatar;
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
	                    'li',
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

/***/ }

})