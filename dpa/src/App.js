import React, { Component } from 'react';
import parliamentLogo from './parliament.png';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={parliamentLogo} className="App-logo" alt="logo" />
          <p>
            VisGov
          </p>

          <p>
            Parliament Analyzes Made Simple
          </p>
          
        </header>
      </div>

    );
  }
}

export default App;
