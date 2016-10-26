/**
 * Created by jmpews on 2016/10/14.
 */

import * as types from '../constants/ActionTypes'

const prefix = 'chat/';

import {
    send_socket_message
} from '../utils'

export const updateRecentUserList = (recent_user_list) => (dispatch, getState) => {
    console.log('updateRecentUserList', recent_user_list);
    dispatch({
        type: types.RECENT_USER_LIST,
        payload: recent_user_list
    });
};

export const setCurrentUser = (id, avatar , name) => (dispatch, getState) => {
    console.log('set_current_user');
    dispatch({
        type: types.SET_CURRENT_USER,
        payload: {
            id: id,
            avatar: avatar,
            name: name
        }
    });

    send_socket_message('update_recent_message_list', {'user_id': id});
};

export const updateRecentMessageList = (recent_message_list) => (dispatch, getState) => {
    dispatch({
        type: types.RECENT_MESSAGE_LIST,
        payload: recent_message_list
    });
};
export const receiveAMessage = (message) => (dispatch, getState) => {
    dispatch({
        type: types.RECEIVE_A_MESSAGE,
        payload: message
    });
};
