import React, {useState} from 'react';
import HomePage from "./HomePage";
import {Link, Element, Events, scroller, animateScroll as scroll} from 'react-scroll';
import CreateDataVis from './DataVis';




function MainPage () {
    const [VisStarted, setVisStarted] = useState(false)
    const [pages, setPages] = useState([0, 1, 2, 3])
    function HandleStartVis () {
        if (VisStarted === false){
        setVisStarted(true)}
        else {
            setVisStarted(false)
        }
        console.log(VisStarted)
    }

    
    if (VisStarted === false) {
    return (
        <div>
        <HomePage />
            <div className="StartVis">
                <h2>Curios about what we have in our pockets?</h2>
                <Link
                    activeClass="active"
                    to={"Section0"}
                    spy={true}
                    smooth={true}
                    offset={-100}
                    duration={800}
                    delay={100}>
                        <button onClick ={HandleStartVis} id='btn-startvis' className="btn btn-info">Click here!</button>
                </Link>  
                <div id='Section0'>
                    </div>  
            </div>

    </div>
        )}
        else {
            return (
                <div>
            <nav className="navbar navbar-default navbar-fixed-top">
            <div className="container-fluid">
              <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul className="nav navbar-nav">{
                    pages.map(
                      page =><li key={"li_"+page}>
                          <Link  activeClass="active" className="test1" to={"Section"+page} offset={-50}
                          spy={true} smooth={true} duration={1000} delay={50}>{"Section"+page}</Link>
                          </li>
                    )
                  }
                    <li onClick ={HandleStartVis}>
                        <Link
                            to={"Section0"}
                            spy={true}
                            smooth={true}
                            offset={0}
                            duration={800}
                            delay={100}>
                            Back on top
                        </Link> 
                    </li>
                  </ul>
            </div>
            </div>
          </nav>
                    <HomePage />
                    <div className="StartVis">
                        <h2>Curios about what we have in our pockets?</h2>
   
                    </div>

               <div>
                        {
                        pages.map(
                        page => 
                            <Element key = {"key_n"+page} className='sections' name={"Section"+page}>
                                <CreateDataVis n_page={page}/>
                            </Element>
                        )
                    }
                    </div>
        </div>
            )
        }
    
    };

export default MainPage;