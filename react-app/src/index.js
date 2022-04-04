import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import CreateHome from './Home.js';
import 'bootstrap/dist/css/bootstrap.min.css';


function App () {
  return (
    <div>
      <CreateHome />
    </div>
  )
}



ReactDOM.render(
  <App />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
