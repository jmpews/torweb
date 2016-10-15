webpackHotUpdate(0,{

/***/ 77:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

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

	var _chatContainer = __webpack_require__(281);

	var _chatContainer2 = _interopRequireDefault(_chatContainer);

	var _ActionTypes = __webpack_require__(280);

	var _chat = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"../api/chat\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	var middleware = [_reduxThunk2.default];

	var store = (0, _redux.createStore)(_index2.default, _redux.applyMiddleware.apply(undefined, middleware));

	store.dispatch({
	  type: _ActionTypes.SEND_UPDATE_RECENT_MESSAGE,
	  payload: _chat.recent_message
	});

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

/***/ }

})