var React = require('react');

class MessageList extends React.Component {
  render() {
      var _this = this;
      var messages = this.props.data.map(function(message, index) {
          var message_type = '';
          var img_src = '';
          if(message[0] == '<') {
              message_type = 'chat-other cl';
              img_src = '/assets/images/avatar/' + _this.props.other_avatar;
          }
          else {
              message_type = 'chat-self cl';
              img_src = '/assets/images/avatar/' + _this.props.other_avatar;
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
              <li id="messageList">
                  {messages}
              </li>
          </div>
      )
  }
}

module.exports = MessageList;