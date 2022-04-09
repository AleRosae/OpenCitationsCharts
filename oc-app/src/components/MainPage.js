import React, {useState} from 'react';
import CreatePage from './CreatePage';
import HomePage from "./HomePage";
import Scroll, {Link} from 'react-scroll';
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
                    duration={500}
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
                    <HomePage />
                    <div className="StartVis">
                        <h2>Curios about what we have in our pockets?</h2>
                        <Link
                            activeClass="active"
                            to={"Section0"}
                            spy={true}
                            smooth={true}
                            offset={-100}
                            duration={500}
                            delay={100}>
                                <button onClick ={HandleStartVis} id='btn-startvis' className="btn btn-info">Back on top</button>
                        </Link>    
                    </div>
                <ul className="header">{
                    pages.map(
                      page => <li key = {"key_ul_n"+page}>
                              <Link
                                  activeClass="active"
                                  to={"Section"+page}
                                spy={true}
                                smooth={'easeInQuad'}
                                offset={-50}
                                duration={1000}
                                delay={200}>
                                    {"Section"+page}
                                </Link>
                      </li>
                    )
                  }</ul>
               <div>
                        {
                        pages.map(
                        page => 
                            <div key = {"key_n"+page} className='sections' id={"Section"+page}>
                                <CreateDataVis n_page={page}/>
                            </div>
                        )
                    }

                    </div>

                </div>

                
            )
        }
    
    };

export default MainPage;