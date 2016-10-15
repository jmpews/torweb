webpackHotUpdate(0,{

/***/ 278:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	  value: true
	});

	var _redux = __webpack_require__(248);

	var _chat = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"./chat\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

	var fromChat = _interopRequireWildcard(_chat);

	function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

	/**
	 * Created by jmpews on 2016/10/14.
	 */

	var _default = (0, _redux.combineReducers)({
	  chat: fromChat.default
	});

	exports.default = _default;
	;

	var _temp = function () {
	  if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	    return;
	  }

	  __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/index.js');
	}();

	;

/***/ }

})