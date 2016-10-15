webpackHotUpdate(0,{

/***/ 279:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _ActionTypes = __webpack_require__(280);

	var initialState = {
	    chat: {
	        current_user: {},
	        recent_message_list: [],
	        recent_user_list: []
	    }
	}; /**
	    * Created by jmpews on 2016/10/14.
	    */

	var update_recnet_message_list = function update_recnet_message_list() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState.recent_message_list;
	    var action = arguments[1];

	    switch (action.type) {
	        case _ActionTypes.SEND_UPDATE_RECENT_MESSAGE:
	            console.log('send_update_recent_message');
	        case _ActionTypes.RECV_UPDATE_RECENT_MESSAGE:
	            console.log('recv_update_recent_message');
	            return action.payload;
	        default:
	            return state;
	    }
	};

	// switch action.type
	var chat = function chat() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState;
	    var action = arguments[1];

	    switch (action.type) {
	        case _ActionTypes.CHECK_SEND:
	            return initialState;
	        default:
	            return {
	                current_user: initialState.current_user,
	                recent_user_list: initialState.recent_user_list,
	                recent_message_list: update_recnet_message_list(state.recent_message_list, action)
	            };
	    }
	};
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(initialState, 'initialState', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(update_recnet_message_list, 'update_recnet_message_list', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(chat, 'chat', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');
	}();

	;

/***/ }

})