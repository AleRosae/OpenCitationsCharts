import React from "react";
import CreatePlot from "./CreatePlot";

export default function CreateDataVis(props) {
    const page_properties = {0:{"title":"Initial", "text": "d", "data": "None"}, 1: {"title":"Grafico", "text":"questo invece è un grafico", 
                            "data": "journals"}, 2:{"title":"Altro grafico", "text":"altro testo", "data": "areas_fields"}}
    console.log(props)
    if (props.n_page > 0) {
    return (<div>
        <div className="row">
            <div className="col-sm">
                <h1>{page_properties[props.n_page].title}</h1>
                <CreatePlot type="Bar" page = {props.n_page} data = {page_properties[props.n_page].data}/>
            </div>
            <div className="col-sm">
                <p>{page_properties[props.n_page].text} </p>
            </div>
        </div>
    </div>
    )
    }
    else {
        return (<div>
            <div className="row">
                <div className="col-sm">
                    <h1>{page_properties[props.n_page].title}</h1>
                </div>
                <div className="col-sm">
                    <p>{page_properties[props.n_page].text} </p>
                </div>
            </div>
        </div>
        )  
    }

}