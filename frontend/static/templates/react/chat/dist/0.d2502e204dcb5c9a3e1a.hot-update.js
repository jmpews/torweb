webpackHotUpdate(0,{

/***/ 279:
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
	    value: true
	});

	var _immutable = __webpack_require__(285);

	var _ActionTypes = __webpack_require__(280);

	/**
	 * Created by jmpews on 2016/10/14.
	 */
	var initialState = {
	    chat: {
	        current_user: {},
	        recent_message_list: [],
	        recent_user_list: []
	    }
	};

	var update_recnet_message_list = function update_recnet_message_list() {
	    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState.recent_message_list;
	    var action = arguments[1];

	    switch (action.type) {
	        case _ActionTypes.RECENT_MESSAGE_LIST:
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
	        case _ActionTypes.RECEIVE_A_MESSAGE:
	            var message = action.payload;
	            if (state.current_user.id != message.id) {
	                var x = (0, _immutable.fromJS)(state);
	                var y = x.getIn(['chat', 'recent_user_list']);
	                var z = r.concat([message]);
	                return x.setIn(['chat', 'recent_user_list'], z).toJS();
	            }
	        case _ActionTypes.RECENT_USER_LIST:
	            return (0, _immutable.fromJS)(state).setIn(['chat', 'recent_user_list'], (0, _immutable.fromJS)(action.payload)).toJS();

	        default:
	            return {
	                chat: {
	                    current_user: state.current_user,
	                    recent_user_list: state.recent_user_list,
	                    recent_message_list: update_recnet_message_list(state.recent_message_list, action)
	                }
	            };
	    }
	};

	var _default = chat;
	exports.default = _default;
	;

	var _temp = function () {
	    if (typeof __REACT_HOT_LOADER__ === 'undefined') {
	        return;
	    }

	    __REACT_HOT_LOADER__.register(initialState, 'initialState', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(update_recnet_message_list, 'update_recnet_message_list', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(chat, 'chat', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');
	}();

	;

/***/ }

})