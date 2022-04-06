import React, {useState} from 'react';
import CreatePage from './CreatePage';
import HomePage from "./HomePage";




function MainPage () {
    const [VisStarted, setVisStarted] = useState(false)
    function HandleStartVis () {
        setVisStarted(!VisStarted)

        console.log(VisStarted)
    }
    
    if (VisStarted === false) {
    return (
    <div>
        <HomePage />
            <div className="StartVis">
                <h2>Curios about what we have in our pockets?</h2>
                <button onClick ={HandleStartVis} id='btn-startvis' className="btn btn-info">Click here!</button>
        </div>
    </div>
    )}
    else {
        return (
        <div>
            <button onClick ={HandleStartVis} id='btn-startvis' className="btn btn-info">Back to Home</button>
            <CreatePage n_page = {1} />
        </div>)
    }

};

export default MainPage;
