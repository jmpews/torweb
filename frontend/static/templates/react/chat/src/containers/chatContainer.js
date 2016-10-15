import React, { ProTypes } from 'react'
import { bindActionCreators } from 'redux';

import { connect } from 'react-redux'

var MessageList = require('../components/messageList.js');
var UserList = require('../components/userList.js');

import {
    updateRecentUserList,
    updateRecentMessageList,
    setCurrentUser
} from '../actions/index'

class ChatContainer extends React.Component {
    constructor(props) {
        super(props);
		this.state = this.props;
		console.log('ChatContainer-constructor.')
    }

    componentDidMount() {
    }

    componentWillMount() {
        // console.log('willMount:',this.props);
        // let { state, dispatch } = this.props;
        // var rm = [
        //     {
        //         id: 1,
        //         avatar: '/admin.png',
        //         name: 'admin'
        //     },
        //     {
        //         id: 1,
        //         avatar: '/admin.png',
        //         name: 'admin'
        //     }
        // ];
        // dispatch(updateRecentUserList(rm));
    }
    render() {
        let { state, dispatch, setCurrentUser} = this.props;
        var _this = this;
        var current_user = state.current_user;
        var chat_title = '';
        if(current_user.id == -1) {
            chat_title = 'real-time-chat';
        }
        else {
            chat_title = 'chat 2' + current_user.name;
        }
        return (
            <div className="chat">
                <div className="chat-header">
                    <a href="#blank" className="chat-title">{chat_title}</a>
                    <a href="#blank" className="chat-close">X</a>
                </div>
                <div className="chat-content">
                    <UserList recent_user_list={state.recent_user_list} setCurrentUser={setCurrentUser} />
                    <MessageList recent_message_list={state.recent_message_list} />
                </div>
                <div className="chat-footer">
                    <form className="form-group row">
                        <textarea className="form-control" cols="2">Write Here.</textarea>
                        <button type="submit" className="btn btn-primary col-sm2">发送</button>
                    </form>
                </div>
            </div>
        );
    }
}

// 从总的store树分离出我们需要的state
function select(state) {
    return {
        state: state.chat
    }
}

// 注入actions
function mapDispatchToProps(dispatch) {
    return {
        // updateRecentUserList: bindActionCreators(updateRecentUserList, dispatch),
        // updateRecentMessageList: bindActionCreators(updateRecentMessageList, dispatch),
        setCurrentUser: bindActionCreators(setCurrentUser, dispatch)
    }
}

export default connect(select,mapDispatchToProps)(ChatContainer);
// export default ChatContainer;
