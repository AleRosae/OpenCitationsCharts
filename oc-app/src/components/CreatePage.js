import React from "react";

export default function CreatePage(props){

    return (
        <div>
            <div className="row">
                <div className="col-sm">
                    <h1>Gratico {props.title}</h1>
                </div>
                <div className="col-sm">
                    <p>{props.text}</p>
                </div>
            </div>
        </div>
    )
}