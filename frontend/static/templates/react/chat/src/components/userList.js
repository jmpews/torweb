var React = require('react');
import { store } from '../index'

import {
    SET_CURRENT_USER
} from '../constants/ActionTypes'


class UserList extends React.Component {
    render() {
        var _this = this;
        let { state, setCurrentUser } = this.props;
        var recent_user_list = this.props.recent_user_list;
        var users = null;
        users = recent_user_list.map(function (user, index) {
            var other_id = user.id;
            var other_avatar = '/assets/images/avatar/' + user.avatar;
            var other_name = user.name;
            return (
                <div key={index} className="chat-user" data-other={other_id}
                     onClick={() => setCurrentUser(other_id)}>
                    <img className="chat-user-avatar" src={other_avatar}/>
                    <span className="chat-user-name">{other_name}</span>
                </div>
            )
        });

        return (
            <div className="user-list">
                {users}
            </div>
        )
    }
}

module.exports = UserList;