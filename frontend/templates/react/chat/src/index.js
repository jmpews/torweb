import React from 'react'
import { render } from 'react-dom'
import {Provider} from 'react-redux';
import App from './containers/chatContainer'
import { store } from './globalStore'

import { start_chat_websocket } from './utils'

// start websocket server
start_chat_websocket('127.0.0.1:9000');

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('chat-container')
);
