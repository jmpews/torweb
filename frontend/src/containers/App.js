/* CAUTION: When using the generators, this file is modified in some places.
 *          This is done via AST traversal - Some of your formatting may be lost
 *          in the process - no functionality should be broken though.
 *          This modifications only run once when the generator is invoked - if
 *          you edit them, they are not updated again.
 */
import React, {
  Component,
  PropTypes
} from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import {MainApp} from '../components/Main';
import {changeText,buttonClick} from '../actions/const';
/* Populated by react-webpack-redux:reducer */


/* Populated by react-webpack-redux:reducer
 *
 * HINT: if you adjust the initial type of your reducer, you will also have to
 *       adjust it here.
 */
function mapStateToProps(state) {
  /* Populated by react-webpack-redux:reducer */
  console.log(state);
  const props = {text:state.myApp.text};
  return props; }
function mapDispatchToProps(dispatch) {
  /* Populated by react-webpack-redux:action */
  const actions = { changeText:changeText,buttonClick:buttonClick};
  const actionMap = { actions: bindActionCreators(actions, dispatch) };
  return actionMap;
}
export default connect(mapStateToProps, mapDispatchToProps)(MainApp);
