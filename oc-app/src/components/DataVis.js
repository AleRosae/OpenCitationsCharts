import React from "react";
import data from "../data/final_results.json";

const d = data
console.log(d)
export default function CreateDataVis(props) {
    const my_dict = {0:{"title":"Initial", "text": d.init.cited}, 1: {"title":"Grafico", "text":"questo invece è un grafico"}}
    console.log(props)
    return (<div>
        <div className="row">
            <div className="col-sm">
                <h1>{my_dict[props.n_page].title}</h1>
            </div>
            <div className="col-sm">
                <p>{my_dict[props.n_page].text} </p>
            </div>
        </div>
    </div>

    )
}