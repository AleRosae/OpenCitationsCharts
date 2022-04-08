import React from "react";
import {BarChart} from 'reaviz';

const my_data= require('../data/final_results.json'); 

export default function CreatePlot(props) {
    console.log(props);
    //console.log(my_data);
    const data_part = props.data
    console.log(data_part)
    console.log(my_data[data_part].slice(0,10));
 if (props.type == "Bar") {
    const MyChart   = () => 
        <BarChart
            height={400}
            width={600}
            data={
                my_data[data_part].slice(0, 10)
            }
        />

        return (
            <div>
                <MyChart />
            </div>)}

};