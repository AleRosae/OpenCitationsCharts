import React from "react";
import {BarChart, PieChart} from 'reaviz';

const my_data = require('../data/final_results.json'); 

export default function CreatePlot(props) {
    console.log(props)
 if (props.type === "bar") {
    var MyChart   = () => 
        <BarChart
            height={400}
            width={600}
            data={
                my_data[props.data].slice(0, 10)
            }
        />}
else if (props.type === 'pie') {
    var MyChart   = () => 
        <PieChart
            height={400}
            width={600}
            data={
                my_data[props.data]
            }
        />}

    return (
        <div>
            <MyChart />
        </div>)};

export function CreateText(props){
    const texts = {0: "Questo è il testo iniziale",
            1: `Questo è il testo per il grafico che parla dei giornali. Il journal con più citazioni è ${my_data.journals[0].key}, con
                ben ${my_data.journals[0].data} citazioni.`,
            2: "Questo è il testo per il grafico che parla delle aree tematiche", 3:"Questo è il grafico delle self cit per journal",
            4:"Questo è il grafico delle self cit per area invece"}

    return (
        <p>{texts[props.page]}</p>
    )
}