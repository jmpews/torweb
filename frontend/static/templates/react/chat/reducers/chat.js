/**
 * Created by jmpews on 2016/10/14.
 */

import {
    SEND_UPDATE_RECENT_MESSAGE,
    RECV_UPDATE_RECENT_MESSAGE
} from '../constants/ActionTypes'

const initialState = {
    current_user:{},
    recent_message_list: [],
    recent_user_list: []
}

const update_recnet_message_list = (state = initialState.recent_message_list, action) => {
    switch (action.type) {
        case SEND_UPDATE_RECENT_MESSAGE:
            console.log('send_update_recent_message')
        case RECV_UPDATE_RECENT_MESSAGE:
            console.log('recv_update_recent_message')
            return action.payload
        default:
            return state
    }
}
