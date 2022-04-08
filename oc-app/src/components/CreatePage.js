import React, {useState} from "react";
import NavBar from "./NavBar";
import CreateDataVis from "./DataVis";


export default function CreatePage(){
    const [Page, setPage] = useState(0)
    const [Min, Max] = [0, 2]
    function handlePrev() {
        if (Page > Min) {
        setPage((Page) => {
            return Page - 1}
        )}

       // console.log(Page)
    }
    function handleProx() {
        if (Page < Max) {
        setPage((Page) => {
            return Page + 1}
        )};

        //console.log(Page)
    }
    return (
        <div>   
            <NavBar />
            <CreateDataVis n_page = {Page}/>
                <div>
                    <button onClick={handlePrev}>Prev</button>
                    <button onClick={handleProx}>Prox</button>
                </div>
                </div>
    )

    }
