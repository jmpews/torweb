var React = require('react');

class UserList extends React.Component {
  render() {
      var _this = this;
      var recent_user_list = this.props.recent_user_list;
      var users = this.props.data.map(function(user, index) {
          var other_id = recent_user_list.user.other_id;
          var other_avatar = '/assets/images/avatar/' + recent_user_list.user.other_avatar;
          var other_name = recent_user_list.user.other_name;
          return (
              <div key={index} className="chat-user" other={other_id}>
                  <img className="chat-user-avatar" src={other_avatar} />
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