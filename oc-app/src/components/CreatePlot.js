import React, { PureComponent }  from "react";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie } from 'recharts';
import ScrollAnimation from 'react-animate-on-scroll';

const my_data = require('../data/final_results.json'); 


export default function CreatePlot(props) {
    console.log(props)
 if (props.type === "bar") {
    var MyChart   = () => (
            <BarChart key={"chart_bar_"+props.n_clic} width={800} height={600} data={my_data[props.data].slice(0, 10)} isAnimationActive={true}>
            <XAxis dataKey="key" angle={-45} textAnchor="end" interval={0}/>
            <YAxis dataKey="data" />
            <Legend />
            <Bar dataKey="data" fill="#82ca9d" />
            <Tooltip  animationBegin={20000} animationDuration={10000} animationEasing={'easy-in'}/>

            </BarChart>
)}
        

else if (props.type === 'pie' && props.data == "areas_groups") {
    var MyChart   = () => 
        <PieChart width={800} height={600} isAnimationActive={false}>
        <Pie data={my_data[props.data]} nameKey="key" dataKey="data" cx="50%" cy="50%" outerRadius={160} fill="#8884d8" />
        <Pie data={my_data["areas_supergroups"]} dataKey="data" nameKey="key"  cx="50%" cy="50%" innerRadius={180} outerRadius={240} fill="#82ca9d" label />
        <Tooltip />
        </PieChart>}
        
else if (props.type === 'pie') {
    var MyChart   = () => 
        <PieChart width={800} height={600} isAnimationActive={false}>
        <Pie data={my_data[props.data]} dataKey="data" nameKey="key" cx="50%" cy="50%"  outerRadius={200} fill="#82ca9d" label />
        <Tooltip />
        </PieChart>}



    return (
            <MyChart />
            )};

export function CreateText(props){
const texts = {0: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vulputate leo vel pulvinar maximus. Suspendisse rutrum  dolor id lacus aliquet molestie. Mauris nec orci vel nisl blandit cursus ut non lacus. Phasellus eu libero purus. Curabitur hendrerit velit id eros lacinia, tincidunt finibus dui pretium. Duis tristique felis commodo quam porta faucibus. Aliquam ullamcorper urna vel ex elementum, id feugiat ipsum luctus. Praesent scelerisque varius mauris a tristique. Morbi congue ornare ante, posuere congue ligula placerat sit amet. Praesent posuere leo nisl, et molestie tellus pulvinar eget. Maecenas convallis neque ut lacus dignissim, in vestibulum urna consequat. Nulla facilisi. Phasellus non ex a magna dapibus luctus id ut velit. In at risus fringilla libero fringilla laoreet. Donec consectetur orci eu velit pretium, accumsan bibendum ligula consectetur. Vivamus aliquam vel risus sed malesuada.",
            1: `Questo è il testo per il grafico che parla dei giornali. Il journal con più citazioni è ${my_data.journals[0].key}, con
                ben ${my_data.journals[0].data} citazioni.`,
            2: "Questo è il testo per il grafico che parla delle aree tematiche", 3:"Questo è il grafico delle self cit per journal",
            4:'Questo è il grafico delle self cit per area invece', 5: `The chart displays the fields that received the most number of citations in 2020. It represents the main themes and subjects that are covered by the articles that were published in 2020 The most popular field is ${my_data.areas_fields[0].key}, with the astonishing number of ${my_data.areas_fields[0].data} citations. The least popular one is ${my_data.areas_fields[my_data.areas_fields.length-1].key}, which received only ${my_data.areas_fields[my_data.areas_fields.length-1].data} mentions.`, 6: `The subdivision of the 325 fields present in the COCI dataset in groups. The most popular group is ${my_data.areas_groups[0].key} which received ${my_data.areas_groups[0].data} mentions. The least popular one is ${my_data.areas_fields[my_data.areas_groups.length-1].key} with ${my_data.areas_fields[my_data.areas_groups.length-1].data} citations.`}

    return (
        <ScrollAnimation animateIn="fadeInRight">
            <p className="plotdescr">{texts[props.page]}</p>
        </ScrollAnimation>
    )
}