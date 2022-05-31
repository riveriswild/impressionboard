import React from 'react';
import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import {TweetsComponent} from './tweets'
import reportWebVitals from './reportWebVitals';

//const appEl = document.getElementById('root')
const appEl = document.getElementById('root');
if (appEl) {
  const root = createRoot(appEl);
  root.render(<App />)
}

const tweetsEl = document.getElementById("tweetme-2")
if (tweetsEl) {
  const root = createRoot(tweetsEl);
  root.render(<TweetsComponent />)

}
// const tweetsEl = document.getElementById('tweetme-2')
// if (tweetsEl) {
//   ReactDOM.render(<TweetsComponent />, tweetsEl)
// }

// reportWebVitals();
