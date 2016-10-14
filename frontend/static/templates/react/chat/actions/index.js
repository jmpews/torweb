/**
 * Created by jmpews on 2016/10/14.
 */

import * as types from '../constants/ActionTypes'
const prefix = 'chat/';

export const sendUpdateRecentMessage = (userId) => (dispath, getState) => {
    dispath({
        type: types.SEND_UPDATE_RECENT_MESSAGE,
        payload: userId
    });
}

export const recvUpdateRecentMessage = (data) => ({
    type: types.RECV_UPDATE_RECENT_MESSAGE,
    payload: data
})