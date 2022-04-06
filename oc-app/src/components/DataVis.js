import React from "react";
import CreatePlot from "./CreatePlot";

export default function CreateDataVis(props) {
    const my_dict = {0:{"title":"Initial", "text": "d"}, 1: {"title":"Grafico", "text":"questo invece è un grafico"}}
    console.log(props)
    return (<div>
        <div className="row">
            <div className="col-sm">
                <h1>{my_dict[props.n_page].title}</h1>
                <CreatePlot type="Bar"/>
            </div>
            <div className="col-sm">
                <p>{my_dict[props.n_page].text} </p>
            </div>
        </div>
    </div>

    )
}