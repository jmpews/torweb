webpackHotUpdate(0,{

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

/***/ }

})