import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import reducer from './reducers/index'
const middleware = [ thunk ];

export const store = createStore(
  reducer,
  applyMiddleware(...middleware)
);

