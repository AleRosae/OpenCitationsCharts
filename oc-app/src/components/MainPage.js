import React, {useState, useRef} from 'react';
import HomePage from "./HomePage";
import {Link, Element, Events, scroller, animateScroll as scroll} from 'react-scroll';
import CreateDataVis from './DataVis';


function MainPage () {
    const [pages, setPages] = useState([0, 1, 2, 3, 4])
    const [n_clic, set_nclic] = useState(0)
    console.log(n_clic)

    function handleChange (start) {
        if (start != false) {
        console.log("triggered");
        set_nclic(n_clic+1);
        return (pages.map(page => 
            <Element key = {"key_n"+page} className='sections' name={"Section"+page} >
                <CreateDataVis n_page={page} n_clic={n_clic}/>
            </Element>)) 
            }
        else {
            console.log("triggered");
            return (pages.map(page => 
                <Element key = {"key_n"+page} className='sections' name={"Section"+page} >
                    <CreateDataVis n_page={page} n_clic={n_clic}/>
                </Element>)) 
                }  
        }
   
    return (
        <div>
    <nav className="navbar navbar-expand-md fixed-top navbar-light bg-light">
        <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul className="navbar-nav">
            <li key={"Main"} className='nav-item active'> <Link  activeClass="nav-item active" className="nav-link" to={"Main"} offset={-50}
                    spy={true} smooth={true} duration={1200} delay={150}>{"Home"}</Link></li>
            {pages.map(
                page =><li key={"li_"+page}>
                    <Link  onClick={handleChange} activeClass="nav-item active" className="nav-link" to={"Section"+page} offset={-50}
                    spy={true} smooth={true} duration={1000} delay={100}>{"Section"+page}</Link>
                    </li>
            )
            }
            </ul>
        </div>
    </nav>
            <HomePage />
            <div className="StartVis">
                <h2>Curios about what we have in our pockets?</h2>
            </div>

        <div>
           {handleChange(false)}
        </div>
</div>
            )    
    };

export default MainPage;