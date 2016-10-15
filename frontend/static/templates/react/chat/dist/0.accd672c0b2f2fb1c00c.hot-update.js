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
	        current_user: {
	            id: -1,
	            name: '',
	            avatar: ''
	        },
	        recent_message_list: [],
	        recent_user_list: []
	    }
	};

	var update_recent_message_list = function update_recent_message_list() {
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
	            return initialState;
	            var message = action.payload;
	            var x = (0, _immutable.fromJS)(state);
	            if (state.current_user.id != message.id) {
	                var y = x.getIn(['chat', 'recent_user_list']);
	                var z = r.push(message);
	                return x.setIn(['chat', 'recent_user_list'], z).toJS();
	            } else {
	                var y = x.getIn(['cha', 'recent_message_list', 'msg']);
	                var z = y.push(['<', message.contnet]);
	                return x.setIn(['cha', 'recent_message_list', 'msg'], z).toJS();
	            }
	        case _ActionTypes.RECENT_USER_LIST:
	            return initialState;
	            return (0, _immutable.fromJS)(state).setIn(['chat', 'recent_user_list'], action.payload).toJS();
	        case _ActionTypes.SET_CURRENT_USER:
	            return initialState;
	            return (0, _immutable.fromJS)(state).setIn(['chat', 'current_user'], action.payload).toJS();
	        default:
	            return initialState;
	            return (0, _immutable.fromJS)(state).toJS();
	        // debugger;
	        // var x = fromJS(state);
	        // var y = x.setIn(['chat','recent_message_list'], [1]);
	        // var z = y.toJS();
	        // return z;
	        // return fromJS(state).setIn(['chat', 'recent_message_list'], update_recent_message_list(state.recent_message_list, action)).toJS();
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

	    __REACT_HOT_LOADER__.register(update_recent_message_list, 'update_recent_message_list', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(chat, 'chat', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');

	    __REACT_HOT_LOADER__.register(_default, 'default', '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates/react/chat/src/reducers/chat.js');
	}();

	;

/***/ }

})