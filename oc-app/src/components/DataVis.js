import React from "react";
import CreatePlot, {CreateText} from "./CreatePlot";
import ScrollAnimation from 'react-animate-on-scroll';


export default function CreateDataVis(props) {
    const page_properties = {0:{"title":"Initial", "data": "None"}, 1: {"title":"Grafico", "type": "bar",
                            "data": "journals"}, 2:{"title":"Altro grafico", "type": "bar", "data": "areas_fields"},
                            3:{"title": "Self citation journals", "type":"pie", "data": "self_cit_journals"},
                            4:{"title": "Self citation area", "type":"pie", "data": "self_cit_area"}}
    console.log(props)
    if (props.n_page > 0) {
    return (
        <div className="row">
            
                <h1>{page_properties[props.n_page].title}</h1>
                <ScrollAnimation animateIn='slideInLeft' animateOut="slideOutLeft" duration={2}
                                 delay={0}>
                    <CreatePlot type={page_properties[props.n_page].type}  data = {page_properties[props.n_page].data}/>
                </ScrollAnimation>

                <ScrollAnimation animateIn='slideInRight' animateOut="slideOutRight" duration={2}
                                 delay={200}>
                    <CreateText page={props.n_page}/>
            </ScrollAnimation>
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