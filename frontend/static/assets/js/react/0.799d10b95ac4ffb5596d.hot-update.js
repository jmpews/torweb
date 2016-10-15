webpackHotUpdate(0,{

/***/ 77:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _react = __webpack_require__(78);

	var _react2 = _interopRequireDefault(_react);

	var _reactDom = __webpack_require__(110);

	var _reactRedux = __webpack_require__(267);

	var _chatContainer = __webpack_require__(266);

	var _chatContainer2 = _interopRequireDefault(_chatContainer);

	var _globalStore = __webpack_require__(278);

	var _globalStore2 = _interopRequireDefault(_globalStore);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	//---
	start_chat_websocket('127.0.0.1:9000');

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

/***/ }

})