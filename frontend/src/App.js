import React, {useEffect, useState} from 'react';

import logo from './logo.svg';
import './App.css';

import {TweetsComponent} from './tweets'


function App() {

  return (
    <div className="App">
      <header className="App-header">
      <TweetsComponent />
      </header>

    </div>
  );
}

export default App;
