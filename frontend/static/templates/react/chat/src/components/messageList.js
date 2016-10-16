var React = require('react');

class MessageList extends React.Component {
  render() {
      var _this = this;
      var recent_message = this.props.recent_message_list;
      var message_list = recent_message.msg;
      var messages = message_list.map(function(message, index) {
          var message_type = '';
          var img_src = '';
          if(message[0] == '<') {
              message_type = 'chat-other cl';
              img_src = '/assets/images/avatar/' + recent_message.avatar;
          }
          else {
              message_type = 'chat-self cl';
              img_src = '/assets/images/avatar/default_avatar.png';
          }

          return (
              <li key={index} className={message_type}>
                  <img className="avatar" src={img_src} />
                  <div className="chat-text">
                      {message[1]}
                  </div>
              </li>
          )
      });

      return (
          <div className="message-list">
              <ul id="messageList">
                  {messages}
              </ul>
          </div>
      )
  }
}

module.exports = MessageList;