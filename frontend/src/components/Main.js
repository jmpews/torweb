require('normalize.css/normalize.css');
require('styles/App.css');
require('../elemental/less/elemental.less');
import React from 'react';

let yeomanImage = require('../images/yeoman.png');

class AppComponent extends React.Component {
  render() {
    return (
      <div className="index">
        <img src={yeomanImage} alt="Yeoman Generator" />
        <div className="notice">Please edit <code>src/components/Main.js</code> to get started!</div>
      </div>
    );
  }
}

AppComponent.defaultProps = {
};

//Hello
class Hello extends React.Component{
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(){
    this.props.actions.changeText();
  }

  render() {
    return (
      <h1 onClick={this.handleClick}> {this.props.text} </h1>
    );
  }
}

//Change
class Change extends React.Component{
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(){
    this.props.actions.buttonClick();
  }

  render() {
    return (
      <button onClick={this.handleClick} >change</button>
    );
  }
}

//MainApp
class MainApp extends React.Component{
  constructor(props) {
    super(props);
  }

  render() {
    console.log(this.props);
    //actions和text这两个props在第5步中会解释
    const { actions, text} = this.props;
    return (
      <div>
        <Hello actions={actions} text={text}/>
        <Change actions={actions}/>
      </div>
    );
  }
}
export {MainApp};
