import React from "react";
//import data from "../data/final_results.json";
import {BarChart} from 'reaviz';


export default function CreatePlot(props) {
    console.log(props)
 if (props.type == "Bar") {
    const MyChart =
        <BarChart
            height={300}
            width={300}
            data={[
            { key: 'DLP', data: 13 },
            { key: 'SIEM', data: 2 },
            { key: 'Endpoint', data: 7 }
            ]}
        />

        return (
            <div>MyChart</div>)}

};