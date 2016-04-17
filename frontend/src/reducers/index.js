/* Combine all available reducers to a single root reducer.
 *
 * CAUTION: When using the generators, this file is modified in some places.
 *          This is done via AST traversal - Some of your formatting may be lost
 *          in the process - no functionality should be broken though.
 *          This modifications only run once when the generator is invoked - if
 *          you edit them, they are not updated again.
 */
import { combineReducers } from 'redux';
import myApp from './test'
/* Populated by react-webpack-redux:reducer */
const reducers = {myApp};
//module.exports = combineReducers(reducers);
//const rootreducers=combineReducers(reducers);
//export default rootreducers;
//
export default function rootreducers(state = {}, action) {
    console.log(state.myApp);
    return {
        myApp: myApp(state.myApp, action)
    };
}
