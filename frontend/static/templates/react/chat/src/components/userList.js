import React from 'react'

import {
    SET_CURRENT_USER
} from '../constants/ActionTypes'


class UserList extends React.Component {
    render() {
        var _this = this;
        let { state, current_user, setCurrentUser } = this.props;
        var recent_user_list = this.props.recent_user_list;
        var users = null;
        users = recent_user_list.map(function (user, index) {
            var other_id = user.id;
            var other_avatar = '/assets/images/avatar/' + user.avatar;
            var other_name = user.name;
            return (
                <div key={index} className="chat-user"
                     onClick={() => setCurrentUser(other_id, other_avatar, other_name)}>
                    <img className="chat-user-avatar" src={other_avatar}/>
                    <span className="chat-user-name">{other_name}</span>
                </div>
            )
        });
        var current = (<div className="current-user" key="current-user">
            <img className="chat-user-avatar" />
            <span className="chat-user-name">{current_user.name} </span>
        </div>);

        return (
            <div className="user-list">
                {current}
                {users}
            </div>
        )
    }
}

module.exports = UserList;