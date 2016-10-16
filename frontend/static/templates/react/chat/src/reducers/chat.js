/**
 * Created by jmpews on 2016/10/14.
 */
import { fromJS } from 'immutable';

// action type
import {
    CHECK_SEND,
    RECENT_USER_LIST,
    RECENT_MESSAGE_LIST,
    RECEIVE_A_MESSAGE,
    SET_CURRENT_USER
} from '../constants/ActionTypes'

// initialState
const initialState = {
    current_user:{
        id: -1,
        name: '',
        avatar: ''
    },
    recent_message_list: {
        id: -1,
        name: '',
        avatar: '',
        msg: []
    },
    recent_user_list: []
};

const update_recent_message_list = (state = initialState.recent_message_list, action) => {
    switch (action.type) {
        case RECENT_MESSAGE_LIST:
            return action.payload;
        default:
            return state
    }
};

// switch action.type
// with immutable to modify and return the copy of store
// 通过immutable, 来实现修改和返回store的副本
const chat = (state = initialState, action) => {
    switch (action.type) {
        case CHECK_SEND:
            return initialState;
        case RECEIVE_A_MESSAGE:
            var message = action.payload;
            var x = fromJS(state);
            console.log('receieve_a_message:', message);
            if(state.current_user.id != message.id) {
                var y = x.getIn(['recent_user_list']);
                var z = r.push({id: message.id, name: message.name, avatar: message.avatar});
                return x.setIn(['recent_user_list'], z).toJS();
            }
            else {
                var y = x.getIn(['recent_message_list', 'msg']);
                var z = y.push(message.msg);
                return x.setIn(['recent_message_list', 'msg'], z).toJS();
            }
        case RECENT_USER_LIST:
            return fromJS(state).setIn(['recent_user_list'], action.payload).toJS();
        case SET_CURRENT_USER:
            console.log('set_current_user:', action.payload);
            return fromJS(state).setIn(['current_user'], action.payload).toJS();
        case RECENT_MESSAGE_LIST:
            return fromJS(state).setIn(['recent_message_list'], update_recent_message_list(state.recent_message_list, action)).toJS();
        default:
            return fromJS(state).toJS();
    }
};

export default chat
