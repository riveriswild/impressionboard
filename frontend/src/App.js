import React, {useEffect, useState} from 'react';

import logo from './logo.svg';
import './App.css';

function loadTweets(callback) {
  const xhr = new XMLHttpRequest();
  const method = 'GET';
  const url = "/api/tweets"
  const responseType = 'json';
  xhr.responseType = responseType;
  xhr.open(method, url)
  xhr.onload = function () {
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = function (e) {
    callback({"message": "The request was an error"}, 400)
  }
  xhr.send()
}

function App() {
  const [tweets, setTweets] = useState([])

 useEffect(() => {
   // do lookup
   const myCallback =(response, status) => {
     if (status === 200) {
      setTweets(response)
     }

  }
   loadTweets(myCallback)

 }, [])

  return (
    <div className="App">
      <header className="App-header">
       
      </header>
      {tweets.map((tweet, index) => {
        return <li>{tweet.content}</li>
      })}
    </div>
  );
}

export default App;
