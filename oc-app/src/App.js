import './App.css';
import MainPage from './components/MainPage'
import { useEffect, useState } from 'react';
import Scroll, {Link} from './components/SmoothScroll';
import CreateDataVis from './components/DataVis';
import NavBar from './components/NavBar';


function App() {
  const [pages, setPages] = useState([0, 1, 2, 3])


  return (
    <div className="App">
      <NavBar/>
      <div id="section1">
      <MainPage/>
      </div>
      <ul className="header">{
        pages.map(
          page => <li key = {page} className={"Section"+page}>
                    <Link
          activeClass="active"
          to="section1"
        spy={true}
        smooth={true}
        offset={-100}
        duration={500}>
            Section 1
        </Link>
            {"Section"+page}
          </li>
        )
      }</ul>
        {
        pages.map(
          page => <div key = {page} className={"Section"+page}>
            <CreateDataVis n_page={page}/>
          </div>
        )
      }

    </div>
  );
}

export default App;
