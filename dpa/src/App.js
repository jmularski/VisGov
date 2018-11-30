import React, { Component } from 'react';
import parliamentLogo from './parliament.png';
import {Header} from './components/Header';
import {Search} from './components/Search';
import './App.css';

class App extends Component {
  render() {
    return (
      
      <div className="App">
        <header className="App-header">

          <div>
            <div>
              <Header/>
            </div>
          </div>

          <div>
            <div className="col-xs-5 col-xs-offset-1">
              <Search/>
            </div>
          </div>
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
