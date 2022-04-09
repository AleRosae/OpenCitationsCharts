import './App.css';
import MainPage from './components/MainPage'
import { useEffect, useState } from 'react';
import Scroll, {Link} from 'react-scroll';
import CreateDataVis from './components/DataVis';
import NavBar from './components/NavBar';
import ScrollAnimation from 'react-animate-on-scroll';


function App() {

  return (
    <div className="App">
      <NavBar/>
      <MainPage/>

    </div>
  );
}

export default App;
