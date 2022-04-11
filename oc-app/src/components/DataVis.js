import React from "react";
import CreatePlot, {CreateText} from "./CreatePlot";
import ScrollAnimation from 'react-animate-on-scroll';


export default function CreateDataVis(props) {
    const page_properties = {0:{"title":"Initial", "data": "None"}, 1: {"title":"Grafico", "type": "bar",
                            "data": "journals"}, 2:{"title":"Altro grafico", "type": "bar", "data": "areas_fields"},
                            3:{"title": "Self citation journals", "type":"pie", "data": "self_cit_journals"},
                            4:{"title": "Self citation area", "type":"pie", "data": "self_cit_area"}, 5: {
                                "title":"top 20 fields", "type":"bar", "data": "areas_fields"},
                                6:{"title":"Groups and supergroups subdivion", "type":"pie", "data": "areas_groups"
                            }}
    if (props.n_page > 0) {
    return (
        <div className="container">
        <h2>{page_properties[props.n_page].title}</h2>
            <div className="row">
                    <div className="col col-md">
                        <CreatePlot type={page_properties[props.n_page].type} n_clic={page_properties[props.n_page].title+"_"+props.n_clic} data = {page_properties[props.n_page].data}/>
                    </div>
                    <div className="col col-md">
                        <CreateText page={props.n_page}/>
                    </div>
            </div>
        </div>
    )
    }
    else {
        return (
            <div className="row">
                    <h1>{page_properties[props.n_page].title}</h1>
                        <CreateText page={props.n_page}/>
            </div>
        )  
    }

}