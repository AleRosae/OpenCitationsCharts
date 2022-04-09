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
const texts = {0: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vulputate leo vel pulvinar maximus. Suspendisse rutrum  dolor id lacus aliquet molestie. Mauris nec orci vel nisl blandit cursus ut non lacus. Phasellus eu libero purus. Curabitur hendrerit velit id eros lacinia, tincidunt finibus dui pretium. Duis tristique felis commodo quam porta faucibus. Aliquam ullamcorper urna vel ex elementum, id feugiat ipsum luctus. Praesent scelerisque varius mauris a tristique. Morbi congue ornare ante, posuere congue ligula placerat sit amet. Praesent posuere leo nisl, et molestie tellus pulvinar eget. Maecenas convallis neque ut lacus dignissim, in vestibulum urna consequat. Nulla facilisi. Phasellus non ex a magna dapibus luctus id ut velit. In at risus fringilla libero fringilla laoreet. Donec consectetur orci eu velit pretium, accumsan bibendum ligula consectetur. Vivamus aliquam vel risus sed malesuada. ",
            1: `Questo è il testo per il grafico che parla dei giornali. Il journal con più citazioni è ${my_data.journals[0].key}, con
                ben ${my_data.journals[0].data} citazioni.`,
            2: "Questo è il testo per il grafico che parla delle aree tematiche", 3:"Questo è il grafico delle self cit per journal",
            4:"Questo è il grafico delle self cit per area invece"}

    return (
        <p>{texts[props.page]}</p>
    )
}