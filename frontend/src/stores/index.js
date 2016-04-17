const redux = require('redux');
const reducers = require('../reducers');
import rootreducers from '../reducers/index';

module.exports = function(initialState) {
  const store = redux.createStore(rootreducers, initialState)

  if (module.hot&&0) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('../reducers', () => {
      const nextReducer = require('../reducers')
      store.replaceReducer(nextReducer)
    })
  }

  return store
}
