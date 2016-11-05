import React, { ProTypes } from 'react'
import { bindActionCreators } from 'redux';

import { connect } from 'react-redux'

var MessageList = require('../components/messageList.js');
var UserList = require('../components/userList.js');

import {
    setCurrentUser
} from '../actions/index'

import {send_message} from '../utils'

class ChatContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        var _this = this;
        let { state, dispatch, setCurrentUserDispatch} = this.props;
        $(document).on('chatTo', function(event, user){
            setCurrentUserDispatch(user.id, user.avatar, user.name);
            $(_this.refs.realchat).show();
        });
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

        let { state, dispatch, setCurrentUserDispatch} = this.props;
        var _this = this;
        var current_user = state.current_user;
        var chat_title = '';
        if(current_user.id == -1) {
            chat_title = '基于websocket实时聊天';
        }
        else {
            chat_title = current_user.name + "...";
        }
        return (
            <div className="chat-launcher">
                <div className="chat" ref="realchat" >
                    <div className="chat-header">
                        <a href="#blank" className="chat-title">{chat_title}</a>
                        <a href="#blank" className="chat-close" onClick={(e) => {console.log($(_this.refs.realchat).hide())}}>关闭</a>
                    </div>
                    <div className="chat-content">
                        <UserList current_user={state.current_user} recent_user_list={state.recent_user_list} setCurrentUser={setCurrentUserDispatch} />
                        <MessageList recent_message_list={state.recent_message_list} />
                    </div>
                    <div className="chat-footer">
                        <form className="form-group row">
                            <textarea className="form-control" cols="2" ref="content">...</textarea>
                            <button type="submit" className="btn btn-primary col-sm2" onClick={(e) => {e.preventDefault();send_message(current_user.id, _this.refs.content.value.trim())}}>发送</button>
                        </form>
                    </div>
                </div>
                <div className="chat-button" onClick={(e) => {console.log($(_this.refs.realchat).show())}}></div>
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
        setCurrentUserDispatch: bindActionCreators(setCurrentUser, dispatch)
    }
}

export default connect(select,mapDispatchToProps)(ChatContainer);
// export default ChatContainer;
