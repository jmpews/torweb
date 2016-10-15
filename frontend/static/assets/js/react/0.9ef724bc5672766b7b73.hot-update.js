webpackHotUpdate(0,{

/***/ 275:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.store = undefined;

	var _redux = __webpack_require__(255);

	var _reduxThunk = __webpack_require__(276);

	var _reduxThunk2 = _interopRequireDefault(_reduxThunk);

	var _index = __webpack_require__(277);

	var _index2 = _interopRequireDefault(_index);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	var middleware = [_reduxThunk2.default];

	var store = exports.store = (0, _redux.createStore)(_index2.default, _redux.applyMiddleware.apply(undefined, middleware));
	;

	var _temp = function () {
	  if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	    return;
	  }

	  __REACT_HOT_LOADER__.register(middleware, 'middleware', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/globalStore.js');

	  __REACT_HOT_LOADER__.register(store, 'store', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/globalStore.js');
	}();

	;

/***/ }

})